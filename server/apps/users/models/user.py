from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    has_activated_email = models.BooleanField(default=False)
