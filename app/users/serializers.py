from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import CharField, EmailField

from users.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    random_user_id = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'name',
            'random_user_id',
            'password',
            'confirm_password',
            'is_staff',
            'is_superuser'
        ]

    def create(self, validated_data):
        print(validated_data)
        if validated_data['password'] != validated_data['confirm_password']:
            raise serializers.ValidationError(
                {'password': ['this field should match confirm password']})

        try:
            phone_number = validated_data['phone_number']
        except:
            phone_number = ''
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            is_staff=validated_data['is_staff'],
            is_superuser=validated_data['is_superuser'],

        )
        user.set_password(validated_data['password'])

        user.save()

        return user

class UserUrlField(serializers.HyperlinkedIdentityField):
    lookup_field = 'random_user_id'


class UserFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields = [
            'random_user_id',
            'username',
            'followers',
            'following',
        ]

class UserFollowersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User 
        fields = [
            'random_user_id',
            'username',
        ]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = UserUrlField(view_name='users:UserDetailAPIView')
    username = serializers.CharField(read_only=True)
    followers = UserFollowersSerializer(many=True)
    following = UserFollowersSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'url',
            'random_user_id',
            'username',
            'email',
            'name',
            'is_active',
            'is_staff',
            'is_superuser',
            'favourite_dish',
            'profile_image',
            'followers',
            'following',
        ]
