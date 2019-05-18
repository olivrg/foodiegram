import django_filters
from rest_framework import generics

from posts.models import Post
from posts.serializers import PostSerializer


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['owner', 'timestamp']
