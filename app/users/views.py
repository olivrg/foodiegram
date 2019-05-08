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
