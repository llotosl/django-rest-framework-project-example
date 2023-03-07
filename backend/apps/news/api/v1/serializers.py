from rest_framework import serializers

from apps.news.models import News, NewsLike, NewsComment, Comment
from apps.users.serializers import PublicCustomUserSerializer


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'subtitle', 'text')


class UserLikeSerializer(serializers.ModelSerializer):  # Serializer for output
    public_field = serializers.CharField()

    class Meta:
        model = NewsLike
        fields = ('id', 'public_field')


class UserCommentSerializer(serializers.ModelSerializer):  # Serializer for output
    user = PublicCustomUserSerializer(read_only=True)
    text = serializers.EmailField()
    parent_comment = serializers.IntegerField(
        required=False, source='parent_comment.id')

    class Meta:
        model = NewsComment
        fields = ('id', 'user', 'text', 'parent_comment')


class CurrentNewsSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField()
    likes_count = serializers.IntegerField()
    last_comment_user_public_field = serializers.EmailField(allow_null=True)

    likes = PublicCustomUserSerializer(many=True, read_only=True)
    comments = UserCommentSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'subtitle', 'text', 'comments',
                  'likes', 'comments_count', 'likes_count', 'last_comment_user_public_field')


class NewsLikeSerializer(serializers.ModelSerializer):  # Serializer for create
    class Meta:
        model = NewsLike
        fields = ('id', 'user')
        extra_kwargs = {
            'user': {'read_only': True},
        }


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'parent_comment')
        extra_kwargs = {
            'user': {'read_only': True},
            'text': {'required': True},
            'parent_comment': {'required': False, 'allow_null': True}
        }


class NewsCommentSerializer(serializers.ModelSerializer):  # Serializer for create
    comment = CommentSerializer(required=True)

    class Meta:
        model = NewsComment
        fields = ('id', 'comment')
