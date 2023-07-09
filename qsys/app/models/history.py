from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from .app_user import AppUser
from .ctf_information import CtfInformation
from .question import CtfQuestion
from .team import CtfTeam


class CtfAnswerHistory(
    ExportModelOperationsMixin("ctf_answer_history"), models.Model
):
    """CTF問題回答履歴"""

    history_id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(CtfQuestion, models.CASCADE)
    user = models.ForeignKey(AppUser, models.CASCADE)
    team = models.ForeignKey(CtfTeam, models.CASCADE, null=True, blank=True)
    ctf = models.ForeignKey(
        CtfInformation,
        models.CASCADE,
        related_name="answer_history",
        null=True,
    )

    content = models.CharField(max_length=1023, help_text="回答内容")
    is_correct = models.BooleanField(default=False, help_text="正解フラグ")

    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = "CTF問題回答履歴"
        app_label = "app"

    def __str__(self):
        return f"{self.answered_at}, {self.user}, {self.question}"
