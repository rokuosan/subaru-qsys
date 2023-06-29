from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinLengthValidator, RegexValidator
from django_prometheus.models import ExportModelOperationsMixin

from .team import CtfTeam


class AppUserManager(BaseUserManager):
    """App User Manager"""
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(username=username)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True

        user.save()

        return user


class AppUser(ExportModelOperationsMixin('app_user'), AbstractBaseUser, PermissionsMixin):
    """App User Model"""
    objects = AppUserManager()

    username = models.CharField(max_length=255, unique=True,
                                validators=[MinLengthValidator(3, ), RegexValidator(r'^[a-zA-Z0-9]+$')])
    team = models.ForeignKey(CtfTeam, models.CASCADE, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        app_label = "app"
        verbose_name = verbose_name_plural = "ユーザー"
