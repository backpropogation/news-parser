from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=25)
    password = serializers.CharField(max_length=20)
    email = serializers.EmailField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Such account already exists")
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value
