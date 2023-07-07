from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from .team import CtfTeam
from .app_user import AppUser
from .ctf_information import CtfInformation
from .question import CtfQuestion


class CtfScore(ExportModelOperationsMixin("ctf_score"), models.Model):
    """CTFスコア"""

    score_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AppUser, models.CASCADE)
    team = models.ForeignKey(
        CtfTeam, models.CASCADE, null=True, blank=True
    )
    ctf = models.ForeignKey(CtfInformation, models.CASCADE,
                            null=True, blank=True)
    question = models.ForeignKey(CtfQuestion, models.CASCADE)

    date = models.DateField(help_text="日付", auto_now_add=True)
    point = models.PositiveIntegerField(help_text="ポイント")

    class Meta:
        app_label = "app"
        verbose_name = verbose_name_plural = "スコア"

    def __str__(self):
        return f"{self.user}, {self.point}"
