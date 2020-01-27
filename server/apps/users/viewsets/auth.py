from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ViewSet

from apps.users.serializers import UserSerializer, UserLoginSerializer
from apps.users.tasks import send_activation_url

User = get_user_model()


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
        serializer = UserLoginSerializer(data=user_data)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(**user_data)
            if user and user.has_activated_email:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'status': 'successfully logined'
                })
            if not cache.get(f'{user.username}_activation_link_resent', False):
                webhook_url = reverse('email-confirm', request=request)
                send_activation_url.apply_async(args=(user.username, user.email, webhook_url), kwargs={'resend': True})
                return Response({
                    'message': 'your email is not activated, check your mail we sent you a message'
                }, status=status.HTTP_403_FORBIDDEN
                )
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(('GET',))
def mail_confirm(request):
    username = cache.get(request.GET.get('confirm'), None)
    if username:
        user = User.objects.get(username=username)
        user.has_activated_email = True
        user.save()
        cache.delete(request.GET.get('confirm'))
        cache.delete(f'{username}_activation_link')
        return Response({"message": "successfully activated"})
    return Response(status=status.HTTP_404_NOT_FOUND)
