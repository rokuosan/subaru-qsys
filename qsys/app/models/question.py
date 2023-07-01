from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from .category import CtfQuestionCategory
from .difficulty import CtfQuestionDifficulty


class CtfQuestion(ExportModelOperationsMixin("ctf_question"), models.Model):
    """CTF問題"""

    question_id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey(CtfQuestionCategory, models.CASCADE)
    title = models.CharField(max_length=255, help_text="問題タイトル")
    content = models.TextField(max_length=8191, help_text="問題文")
    explanation = models.TextField(
        max_length=8191, help_text="解説", blank=True, null=True
    )
    point = models.PositiveBigIntegerField(help_text="配点")
    flag = models.CharField(max_length=1023, help_text="フラグ")
    difficulty = models.ForeignKey(
        CtfQuestionDifficulty, models.CASCADE, help_text="難易度"
    )

    file_path = models.CharField(
        max_length=1023, help_text="問題ファイルパス", blank=True, null=True
    )

    is_published = models.BooleanField(default=False, help_text="公開フラグ")
    is_practice = models.BooleanField(default=False, help_text="練習問題フラグ")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    note = models.TextField(max_length=8191, help_text="備考", blank=True, null=True)

    class Meta:
        app_label = "app"
        verbose_name = verbose_name_plural = "CTF問題"

    def __str__(self):
        return f"{self.category}, {self.title}"
