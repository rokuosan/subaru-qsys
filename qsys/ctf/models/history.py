from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


from app.models.app_user import AppUser


class History(models.Model, ExportModelOperationsMixin("history")):
    """CTF 回答履歴"""
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, help_text="問題"
    )
    user = models.ForeignKey(
        AppUser, on_delete=models.CASCADE, help_text="回答者"
    )
    team = models.ForeignKey(
        "Team", on_delete=models.CASCADE, help_text="チーム"
    )
    is_correct = models.BooleanField(
        help_text="正解したかどうか", default=False
    )
    answer = models.CharField(
        max_length=255, help_text="回答内容", blank=True, default=""
    )
    point = models.PositiveIntegerField(
        help_text="獲得点数", default=0
    )
    result = models.CharField(
        max_length=255, help_text="判定結果", blank=True, default="",
        choices=(
            ("correct", "正解"),
            ("incorrect", "不正解"),
            ("pending", "未判定"),
            ("flag_format_error", "フラグ形式エラー"),
            ("time_limit_exceeded", "時間切れ"),
            ("already_answered", "回答済み"),
        )
    )
    created_at = models.DateTimeField(auto_now_add=True, help_text="回答日時")

    class Meta:
        app_label = "ctf"
        verbose_name = verbose_name_plural = "回答履歴"

    def __str__(self):
        return f"{self.team.name} - {self.question.title}"

    def is_first_answer_in_team(self):
        """チーム内での初回回答かどうかを返す"""
        count = History.objects.filter(
            question=self.question,
            team=self.team,
            is_correct=True,
        ).count()
        return count == 0
