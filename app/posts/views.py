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
