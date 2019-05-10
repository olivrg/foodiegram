from uuid import uuid4

import django_filters
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework import filters, generics, mixins
from rest_framework.authentication import (BasicAuthentication,
                                           SessionAuthentication)
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from users.authentication import (CreateUserAuthentication,
                                  ExampleAuthentication)
from users.forms import MemberFormPersonal, MemberProfilePhotoForm
from users.models import User
from users.permissions import IsOwnerOrSuperUser, IsSuperUser
from users.serializers import (UserCreateSerializer, UserFollowSerializer,
                               UserSerializer)


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username', 'name',
                     'email', 'random_user_id')

    def get_queryset(self):
        user = self.request.user
        # if user is not superuser, return his/her info only
        if user.is_superuser:
            site_users = None
            if not site_users:
                site_users = User.objects.all().order_by('-date_joined')
                cache.set('site_users', site_users, 600)
                print('Not retrieved from cache, but set it')
            else:
                print('Retrieved from cache')

            return site_users
        else:
            return User.objects.filter(username=user.username)

class UserDetailAPIView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = []

    def put(self, request, *args, **kwargs):
        random_user_id = self.kwargs.pop('random_user_id')
        user = get_object_or_404(User, random_user_id=random_user_id)
        if len(request.data) == 2:
            user.profile_picture = request.data['profile_picture']
            user.save()
            return Response(HTTP_200_OK)

        else:
            user.name = request.data['name']
            user.username = request.data['username']
            user.email = request.data['email']
            user.favourite_dish = request.data['favourite_dish']
            user.save()
            return Response(HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        random_user_id = self.kwargs.pop('random_user_id')
        user = get_object_or_404(User, random_user_id=random_user_id)
        tokens = AuthToken.objects.filter(user=user)
        return user

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    authentication_classes = []
    permission_classes = []


class LoggedInUserAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrSuperUser, IsAuthenticated]
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_object(self, *args, **kwargs):
        user = self.request.user
        return user

@api_view(['POST'])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def update_password(request, *args, **kwargs):
    user = get_object_or_404(User, username=request.data['username'])
    current_password = request.data['current_password']
    new_password = request.data['new_password']
    if user.check_password(current_password):
        user.set_password(new_password)
        user.save()

    else:
        return Response({'error': 'Incorrect password'}, status=HTTP_400_BAD_REQUEST)
    return Response({'message': 'Successfully updated password'}, status=200)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def reset_password(request, *args, **kwargs):
    user = get_object_or_404(User, username=request.data['username'])
    user_token = user.reset_password_token
    post_token = request.data['token']
    if post_token == user_token:
        new_password = request.data['password']
        user.set_password(new_password)
        user.reset_password_token = ''
        user.save()
        return Response({'message': 'Your password has updated successfully'}, status=200)
    else:
        return Response({'error': 'This reset password url has expired'}, status=HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def forgot_password(request, *args, **kwargs):
    username_or_email = request.data['user']
    if len(User.objects.filter(username=username_or_email)) == 0:
        if len(User.objects.filter(email=username_or_email)) == 0:
            return Response({'error': 'No user with that username or email exists'}, status=HTTP_400_BAD_REQUEST)
        else:
            user = User.objects.filter(email=username_or_email)[0]
    else:
        user = User.objects.filter(username=username_or_email)[0]

    reset_password_token = uuid4()
    user.reset_password_token = reset_password_token
    user.save()
    subject = 'Reset your Password'
    body_message = 'Click the following link in order to reset your password'
    root_url = 'https://dashboard.foodiegram.com'
    body = '%s: %s/reset-password/%s?token=%s' % (
        body_message, root_url, user.username, reset_password_token)
    send_mail(
        subject,
        body,
        'support@foodiegram.com',
        [user.email]
    )
    return Response({'message': 'Check your email for password reset instructions'}, status=200)
