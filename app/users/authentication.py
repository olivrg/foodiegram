from django.contrib.auth import authenticate
from rest_framework import authentication, exceptions

from users.models import User


class ExampleAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        # Get username and password
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if not username or not password:
            raise exceptions.AuthenticationFailed('No credentials provided.')

        credentials = {
            'username': username,
            'password': password
        }

        user = authenticate(**credentials)

        if user is None:
            raise exceptions.AuthenticationFailed('Invalid username/password.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (user, None)  # authentication successful


class CreateUserAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):

        # Get the username and password
        token = request.data.get('token', None)

        if not token or token != 'foodiegram-create-user':
            raise exceptions.AuthenticationFailed('No credentials provided.')

        return ('success', None)  # authentication successful
