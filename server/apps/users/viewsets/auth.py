from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.users.serializers import UserSerializer


class RegisterViewSet(ViewSet):

    def create(self, request):
        user_data = {
            'username': request.data.get('username', None),
            'password': request.data.get('password', None)
        }
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.create_user(**serializer.validated_data)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'status': 'successfully registered'
            })


class LoginViewSet(ViewSet):

    def create(self, request):
        user_data = {
            'username': request.data.get('username', None),
            'password': request.data.get('password', None)
        }
        user = authenticate(**user_data)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'status': 'successfully logined'
            })
        return Response(status=status.HTTP_401_UNAUTHORIZED)
