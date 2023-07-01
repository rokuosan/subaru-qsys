from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class CtfQuestionDifficulty(
    ExportModelOperationsMixin("ctf_question_difficulty"), models.Model
):
    """CTF問題難易度"""

    difficulty_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, help_text="難易度名")

    class Meta:
        app_label = "app"
        verbose_name = verbose_name_plural = "難易度"

    def __str__(self):
        return self.name
