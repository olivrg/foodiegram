# Generated by Django 2.1.7 on 2019-05-15 07:51

import config.helper
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('random_user_id', models.CharField(default=config.helper.random_id, editable=False, max_length=32, primary_key=True, serialize=False, unique=True, verbose_name='Random User Id')),
                ('username', models.CharField(db_index=True, help_text='Required. 255 characters or fewer. Letters, numbers and             @/./+/-/_ characters', max_length=255, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[\\w.@+-]+$'), 'Enter a valid username.', 'invalid')], verbose_name='Username')),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='Email')),
                ('name', models.CharField(max_length=60, verbose_name='Name')),
                ('favourite_dish', models.CharField(blank=True, max_length=60, null=True, verbose_name='Favourite dish')),
                ('date_joined', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active User')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff User')),
                ('profile_picture', models.CharField(blank=True, default='', max_length=120)),
                ('reset_password_token', models.CharField(blank=True, max_length=120, null=True)),
                ('followers', models.ManyToManyField(blank=True, related_name='followers_field', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='following_field', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
