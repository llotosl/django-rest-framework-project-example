from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.news.models import News, NewsComment, Comment
from apps.news.api.v1.serializers import NewsSerializer
from apps.users.models import CustomUser
from apps.core.pagination import CustomLimitOffsetPagination


class NewsTest(APITestCase):
    def setUp(self) -> None:
        [News.objects.create(
            title='Title1',
            subtitle='Title1',
            text='Text1',
        ) for _ in range(150)]

        # Setting up admin and user for testing.
        self.admin = CustomUser.objects.create_superuser(
            email='js@js.com', password='js.sj')
        self.user = CustomUser.objects.create_user(
            email='js@js1.com', password='js.sj')

        NewsComment.objects.create(
            news=News.objects.first(),
            comment=Comment.objects.create(
                user=self.admin,
                text='sakjdbajksdkjaw'
            )
        )

        # Setting up clients for tests.
        self.admin_client = APIClient()
        refresh = RefreshToken.for_user(self.admin)
        self.admin_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.user_client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.user_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_news_list(self):
        url = reverse('news-list')
        response = self.admin_client.get(url, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response.data.get('results')),
                             CustomLimitOffsetPagination.default_limit)

        response = self.user_client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_news_create(self):
        url = reverse('news-list')

        data = {'title': 'a'*64, 'text': 'd'*2000}
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

        data = {'title': 'a', 'text': 'd'*2001}
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

        data = {'title': 'a'*65, 'text': 'd'}
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

        data = {'title': 'abc', 'text': 'def'}
        response = self.user_client.post(url, data, format='json')
        # No more tests with user because viewset permission is working.
        self.assertEqual(response.status_code, 403)

    def test_news_update(self):
        new = News.objects.first()
        url = reverse('news-detail', kwargs={'pk': new.id})

        data = {'title': 'a'*64, 'text': 'd'*2000}
        response = self.admin_client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        url = reverse('news-detail', kwargs={'pk': 15000})
        response = self.admin_client.put(url, data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_news_partial_update(self):
        new = News.objects.first()
        data = {'text': 'd'*2000}

        url = reverse('news-detail', kwargs={'pk': new.id})
        response = self.admin_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        url = reverse('news-detail', kwargs={'pk': 15000})
        response = self.admin_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_news_delete(self):
        new = News.objects.first()
        url = reverse('news-detail', kwargs={'pk': new.id})
        response = self.admin_client.delete(url, format='json')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(None, News.objects.filter(id=new.id).first())

        url = reverse('news-detail', kwargs={'pk': 15000})
        response = self.admin_client.delete(url, format='json')
        self.assertEqual(response.status_code, 404)

    def test_news_comment_create(self):
        new = News.objects.first()
        url = reverse('news-comment', kwargs={'id': new.id})

        data = {'comment': {'text': 'd'*401}}
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

        data = {'comment': {'text': 'd'*400}}
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        data = {'comment': {'text': 'd'*400, 'parent_comment': 15000}}
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

        comment = NewsComment.objects.first()
        data = {'comment': {'text': 'd'*400, 'parent_comment': comment.id}}
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        url = reverse('news-comment', kwargs={'id': 15000})
        data = {'comment': {'text': 'd'*400}}
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)

    def test_news_like_create(self):
        new = News.objects.first()
        data = {}
        url = reverse('news-like', kwargs={'id': new.id})

        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 204)

        url = reverse('news-like', kwargs={'id': 15000})
        response2 = self.admin_client.post(url, data, format='json')
        self.assertEqual(response2.status_code, 404)

    def test_news_email_send(self):
        data = {}

        new = News.objects.first()
        url = reverse('news-email', kwargs={'id': new.id})
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)

        url = reverse('news-email', kwargs={'id': 15000})
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, 404)
