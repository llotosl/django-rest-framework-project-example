from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.views import Response, APIView
from rest_framework.exceptions import NotFound

from django.db.models import Count

from .serializers import NewsSerializer, CurrentNewsSerializer, NewsLikeSerializer, NewsCommentSerializer
from apps.news.models import News, NewsLike, NewsComment, Comment
from apps.core.permissions import IsAdminOrReadOnly
from .tasks import send_news_to_email


class NewsViewset(viewsets.ModelViewSet):
    queryset = News.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            self.serializer_class = CurrentNewsSerializer
        else:
            self.serializer_class = NewsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action in ('retrieve',):
            return News.objects.prefetch_related('likes', 'comments', 'comments__user').annotate(
                likes_count=Count(
                    'likes',
                    distinct=True
                ),
                comments_count=Count(
                    'comments',
                    distinct=True
                ),
            )

        return super().get_queryset()


class NewsLikeView(CreateAPIView):
    queryset = NewsLike.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = NewsLikeSerializer

    def create(self, request, id: int, *args, **kwargs):
        serializer = NewsLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        news = NewsLike.objects.filter(user=request.user).first()
        if news:
            news.delete()
        else:
            news = NewsLike.objects.create(
                user=request.user,
                news_id=id,
            )

        serializer = NewsLikeSerializer(news)

        return Response(data=serializer.data)


class NewsCommentView(CreateAPIView):
    queryset = NewsComment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = NewsCommentSerializer

    def create(self, request, id: int, *args, **kwargs):
        serializer = NewsCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = Comment.objects.create(
            user=request.user,
            **serializer.validated_data.get('comment')
        )

        news_comment = NewsComment.objects.create(
            news_id=id,
            comment=comment,
        )

        serializer = NewsCommentSerializer(news_comment)

        return Response(data=serializer.data)


class NewsSendToEmailView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, id: int):
        exists = News.objects.filter(
            id=id
        ).exists()
        if not exists:
            raise NotFound('News not found')
        send_news_to_email.delay(id, request.user.email)
        
        return Response(data={'status': 'ok'})
