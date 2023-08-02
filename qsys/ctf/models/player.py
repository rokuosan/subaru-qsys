from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from app.models.app_user import AppUser


class Player(models.Model, ExportModelOperationsMixin("player")):
    """CTF プレイヤー"""

    name = models.CharField(max_length=255, help_text="プレイヤー名", unique=True)

    user = models.OneToOneField(
        AppUser, on_delete=models.CASCADE, help_text="ユーザー", unique=True,
        related_name="player"
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = "ctf"
        verbose_name = verbose_name_plural = "プレイヤー"

    def get_player(user: AppUser):
        """ユーザーからプレイヤーを取得する"""
        try:
            return Player.objects.get(user=user)
        except Player.DoesNotExist:
            return None
