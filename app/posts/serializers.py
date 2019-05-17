from rest_framework import serializers

from posts.models import Comment, Post, Report
from users.models import User


class PostUrlField(serializers.HyperlinkedIdentityField):
    lookup_field = 'random_post_id'


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'random_user_id',
            'username',
            'name',
        ]


class PostLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'random_user_id',
            'username',
        ]


class PostSerializer(serializers.HyperlinkedModelSerializer):
    url = PostUrlField(view_name='posts:PostDetailAPIView')
    user = PostUserSerializer()
    likes = PostLikesSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            'url',
            'random_post_id',
            'owner',
            'image',
            'caption',
            'timestamp',
            'likes',
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'owner',
            'image',
            'caption',
        ]


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'random_comment_id',
            'post',
            'owner',
            'content',
            'timestamp',
        ]


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Report
        fields = [
            'random_report_id',
            'post',
            'user',
            'message',
            'timestamp',
        ]
