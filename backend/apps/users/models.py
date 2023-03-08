from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    public_field = models.CharField(max_length=255, default='string')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['public_field']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
