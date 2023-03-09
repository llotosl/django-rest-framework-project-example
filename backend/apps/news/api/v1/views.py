from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework.views import Response, APIView
from rest_framework.exceptions import NotFound, ValidationError

from django.db.models import Count, Subquery, OuterRef

from .serializers import NewsSerializer, CurrentNewsSerializer, NewsLikeSerializer, NewsCommentSerializer
from apps.news.models import News, NewsLike, NewsComment, Comment
from apps.core.permissions import IsAdminOrReadOnly
from .tasks import send_news_to_email
from .filters import NewsFilterSet


class NewsViewset(viewsets.ModelViewSet):
    queryset = News.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    
    filterset_class = NewsFilterSet

    def get_serializer_class(self):
        if self.action in ('retrieve',):
            self.serializer_class = CurrentNewsSerializer
        else:
            self.serializer_class = NewsSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        if self.action in ('retrieve',):
            return News.objects.prefetch_related('likes', 'comments__user').annotate(
                likes_count=Count(
                    'likes',
                    distinct=True
                ),
                comments_count=Count(
                    'comments',
                    distinct=True
                ),
                last_comment_user_public_field=Subquery(
                    NewsComment.objects.select_related('comment__user').filter(
                        news=OuterRef('pk')
                    ).order_by('-pk').values('comment__user__public_field')[:1]
                ),
            )

        return super().get_queryset()


class NewsLikeView(CreateAPIView):
    queryset = NewsLike.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = NewsLikeSerializer

    def create(self, request, id: int, *args, **kwargs):
        status_code = 200
        serializer = NewsLikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not News.objects.filter(id=id).exists():
            raise NotFound('News does not exists.')

        news = NewsLike.objects.filter(user=request.user).first()
        if news:
            news.delete()
            status_code = 204
        else:
            news = NewsLike.objects.create(
                user=request.user,
                news_id=id,
            )

        serializer = NewsLikeSerializer(news)

        return Response(data=serializer.data, status=status_code)


class NewsCommentView(CreateAPIView):
    queryset = NewsComment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = NewsCommentSerializer

    def create(self, request, id: int, *args, **kwargs):
        serializer = NewsCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not News.objects.filter(id=id).exists():
            raise NotFound('News does not exists.')

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
            raise NotFound('News does not exists.')
        send_news_to_email(id, request.user.email)

        return Response(data={'status': 'ok'})
