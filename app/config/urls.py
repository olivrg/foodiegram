"""foodiegram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
# from django.contrib.auth.views import logout
from django.contrib.sitemaps.views import sitemap
from django.http.response import HttpResponseServerError
from django.shortcuts import render_to_response
from django.template import Context, loader
from django.urls import path
from knox import views as knox_views
from rest_framework import routers

from app.views import LoginView, api_home

# DRF URLs
router = routers.DefaultRouter()

urlpatterns = [
    url(r'^api/v1/$', api_home,
        name='api_home'),
    url(r'^api/v1/login', LoginView.as_view(),
        name='knox_login'),
    url(r'^api/v1/logout', knox_views.LogoutView.as_view(),
        name='knox_logout'),
    url(r'^api/v1/logoutall', knox_views.LogoutAllView.as_view(),
        name='knox_logoutall'),
    url(r'^api/v1/posts', include(('posts.urls', 'posts'), namespace='posts')),
    url(r'^api/v1/', include(('users.urls', 'users'), namespace='users')),
]

# Django URLs
urlpatterns += [
    url('admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
]
