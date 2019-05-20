import django_filters
from django.shortcuts import get_object_or_404, redirect, render
from knox.auth import TokenAuthentication
from rest_framework import filters, generics, mixins
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from posts.filters import PostFilter
from posts.models import Comment, Post, Report
from posts.serializers import (CommentSerializer, PostCreateSerializer,
                               PostLikesSerializer, PostSerializer,
                               ReportSerializer)
from users.models import User


@api_view(['POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([])
def like_create_api(request, *args, **kwargs):
    serializer = PostLikesSerializer()
    post = get_object_or_404(
        Post, random_post_id=request.data['random_post_id'])
    post.likes.add(request.data['random_user_id'])

    liker = get_object_or_404(
        User, random_user_id=request.data['random_user_id'])
    likee = get_object_or_404(User, random_user_id=post.user.random_user_id)

    return Response(serializer.data, status=HTTP_200_OK)


@api_view(['POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([])
def like_delete_api(request, *args, **kwargs):
    serializer = PostLikesSerializer()
    post = get_object_or_404(
        Post, random_post_id=request.data['random_post_id'])
    user = get_object_or_404(
        User, random_user_id=request.data['random_user_id'])
    post.likes.remove(user)

    liker = user
    likee = get_object_or_404(User, random_user_id=post.user.random_user_id)

    return Response(serializer.data, status=HTTP_200_OK)


class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer 
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = []
    filter_class = PostFilter 
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('owner')

    def get_queryset(self):
        post = Post.objects.all().order_by('timestamp')
        return posts

class PostDetailAPIView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = []

    def put(self, request, *args, **kwargs):
        random_post_id = self.kwargs.pop('random_post_id')
        post = get_object_or_404(Post, random_post_id=random_post_id)
        post.caption = request.data['caption']
        post.save()
        return Response(HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        random_post_id = self.kwargs.pop('random_post_id')
        post = get_object_or_404(Post, random_post_id=random_post_id)
        return post


class PostCreateAPIView(generics.CreateAPIView):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = []
