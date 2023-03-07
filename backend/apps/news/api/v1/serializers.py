from rest_framework import serializers

from apps.news.models import News, NewsLike, NewsComment, Comment


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'subtitle', 'text')


class UserLikeSerializer(serializers.ModelSerializer):  # Serializer for output
    email = serializers.EmailField()

    class Meta:
        model = NewsLike
        fields = ('id', 'email')


class UserCommentSerializer(serializers.ModelSerializer):  # Serializer for output
    email = serializers.EmailField(source='user.email')
    text = serializers.EmailField()
    parent_comment = serializers.IntegerField(
        required=False, source='parent_comment.id')

    class Meta:
        model = NewsComment
        fields = ('id', 'email', 'text', 'parent_comment')


class CurrentNewsSerializer(serializers.ModelSerializer):
    comments_count = serializers.IntegerField()
    likes_count = serializers.IntegerField()

    likes = UserLikeSerializer(many=True, read_only=True)
    comments = UserCommentSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'subtitle', 'text', 'comments',
                  'likes', 'comments_count', 'likes_count')


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
