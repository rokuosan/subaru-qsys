from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

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

    class Meta:
        app_label = "app"
        verbose_name = verbose_name_plural = "CTF情報"

    def __str__(self):
        return self.name
