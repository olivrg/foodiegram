from __future__ import unicode_literals

import re

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.core import validators
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

from config import helper


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser,
                     name, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            last_login=now,
            name=name,
            ** extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, name, **extra_fields):
        """creates and saves a new user"""
        if len(name) > 1:
            name = name[0].upper() + name[1:]

        return self._create_user(username, email, password, False, False, name, **extra_fields)

    def create_superuser(self, username, email, password, first_name, last_name):
        """Creates and saves a new supperuser"""
        user = self._create_user(
            username, email, password, True, True, name)
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """custom user model"""
    random_user_id = models.CharField(
        'Random User Id',
        editable=False,
        max_length=32,
        default=helper.random_id,
        unique=True,
        primary_key=True
    )
    username = models.CharField(
        db_index=True,
        verbose_name='Username',
        unique=True,
        max_length=255,
        help_text=_(
            'Required. 255 characters or fewer. Letters, numbers and \
            @/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                _('Enter a valid username.'),
                _('invalid')
            )
        ]
    )
    email = models.EmailField(
        db_index=True, verbose_name='Email', max_length=255, unique=True)
    name = models.CharField(verbose_name='Name', max_length=60)
    favourite_dish = models.CharField(
        'Favourite dish', max_length=60, blank=True, null=True)
    date_joined = models.DateTimeField(
        verbose_name='Updated At', auto_now=True)
    is_active = models.BooleanField(verbose_name='Active User', default=True)
    is_staff = models.BooleanField(verbose_name='Staff User', default=False)
    profile_picture = models.CharField(max_length=120, blank=True, default="")
    following = models.ManyToManyField(
        "self", related_name='following_field', blank=True, symmetrical=False)
    followers = models.ManyToManyField(
        "self", related_name='followers_field', blank=True, symmetrical=False)
    reset_password_token = models.CharField(
        max_length=120, blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    objects = UserManager()

    def __unicode__(self):
        return smart_text(self.name)
