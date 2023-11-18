from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, editable=False, unique=True, default=uuid.uuid4
    )
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    objects = CustomUserManager()
    # discord
    discord_webhook_url = models.URLField(
        max_length=255, blank=True, null=True
    )  # 해당 부분은 선택사항으로 기본 설정.

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
