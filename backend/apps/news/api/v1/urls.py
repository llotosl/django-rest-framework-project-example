from django.urls import (
    include,
    path,
)

from rest_framework.routers import DefaultRouter

from .views import NewsViewset, NewsLikeView, NewsCommentView, NewsSendToEmailView

router = DefaultRouter()
router.register('news', NewsViewset, basename='news')

urlpatterns = [
    path('news/<int:id>/like/', NewsLikeView.as_view(), name='news-like'),
    path('news/<int:id>/comment/', NewsCommentView.as_view(), name='news-comment'),
    path('news/<int:id>/send-email/', NewsSendToEmailView.as_view(), name='news-email'),
    path('', include(router.urls)),
]
