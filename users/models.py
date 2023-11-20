from django.db import models
from .manager import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid

# from teams.models import Team
"""
teams 구현 후 주석 해제
"""


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, editable=False, unique=True, default=uuid.uuid4
    )
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    # team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
