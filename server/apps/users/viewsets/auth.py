from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet

from apps.users.serializers import UserSerializer
from apps.users.tasks import send_activation_url


class RegisterViewSet(ViewSet):

    def create(self, request):
        user_data = {
            'username': request.data.get('username', None),
            'password': request.data.get('password', None),
            'email': request.data.get('email', None)
        }
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.create_user(**serializer.validated_data)
            webhook_url = reverse('email-confirm', request=request)
            send_activation_url.apply_async(args=(user.username, user.email, webhook_url))
            return Response({
                'status': 'success'
            })


class LoginViewSet(ViewSet):

    def create(self, request):
        user_data = {
            'username': request.data.get('username', None),
            'password': request.data.get('password', None),
        }
        user = authenticate(**user_data)
        if user:
            if user.has_activated_mail:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'status': 'successfully logined'
                })
            else:
                # TODO добавить повторную отправку ссылки для подтверждения
                return Response({'активируй мыло'}, status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(('GET',))
def mail_confirm(request):
    if cache.get(request.GET.get('confirm'), None):
        cache.delete(request.GET.get('confirm'))
        return Response({"message": "successfully activated"})
    return Response(status=status.HTTP_404_NOT_FOUND)
