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
