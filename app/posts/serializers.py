from posts.models import Comment, Post, Report
from rest_framework import serializers
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
