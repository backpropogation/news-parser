from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ViewSet

from apps.users.serializers import UserSerializer, UserLoginSerializer
from apps.users.tasks import send_activation_url, resend_activation_url
from apps.users.utils import ResponseStatuses

User = get_user_model()


class RegisterViewSet(ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            user = User.objects.create_user(**serializer.validated_data)
            webhook_url = reverse('email-confirm', request=request)
            send_activation_url.apply_async(args=(user.username, user.email, webhook_url))
            return Response(ResponseStatuses.SUCCESSFULLY_REGISTERED)


class LoginViewSet(ViewSet):
    throttle_classes = [UserRateThrottle]

    def create(self, request):
        serializer = UserLoginSerializer(data=request.POST)
        if serializer.is_valid(raise_exception=True):
            user = authenticate(**serializer.validated_data)
            if user and user.has_activated_email:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    ResponseStatuses.SUCCESSFULLY_LOGINED.update({
                        'token': token.key,
                    })
                )
            if not cache.get(f'{user.username}_activation_link_was_resent', False):
                webhook_url = reverse('email-confirm', request=request)
                resend_activation_url.apply_async(args=(user.username, user.email, webhook_url))
                return Response(ResponseStatuses.EMAIL_NOT_ACTIVATED, status=status.HTTP_401_UNAUTHORIZED)
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
        return Response(ResponseStatuses.SUCCESSFULLY_ACTIVATED)
    return Response(status=status.HTTP_404_NOT_FOUND)
