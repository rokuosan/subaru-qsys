from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from .app_user import AppUser
from .question import CtfQuestion


class CtfInformation(
    ExportModelOperationsMixin("ctf_information"), models.Model
):
    """CTF情報"""

    ctf_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, help_text="CTF名")
    description = models.TextField(help_text="CTF説明")
    start_at = models.DateTimeField(help_text="開始日時")
    end_at = models.DateTimeField(help_text="終了日時")

    questions = models.ManyToManyField(CtfQuestion, help_text="問題", blank=True)
    participants = models.ManyToManyField(AppUser, help_text="参加者", blank=True)

    is_active = models.BooleanField(default=False, help_text="CTF実施状況")

    # CTFが開始しているかどうか
    @property
    def is_started(self):
        return self.start_at <= self.now

    # CTFが終了しているかどうか
    @property
    def is_ended(self):
        return self.end_at <= self.now

    class Meta:
        app_label = "app"
        verbose_name = verbose_name_plural = "CTF情報"

    def __str__(self):
        return self.name
