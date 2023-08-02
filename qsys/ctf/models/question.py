import uuid

from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class Question(models.Model, ExportModelOperationsMixin("question")):
    """CTF 問題"""

    id = models.UUIDField(
        primary_key=True, help_text="問題ID", default=uuid.uuid4, editable=False
    )
    title = models.CharField(max_length=255, help_text="問題タイトル")
    description = models.TextField(help_text="問題文", blank=True, default="")
    flag = models.CharField(max_length=255, help_text="フラグ")
    point = models.PositiveIntegerField(help_text="点数")
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_DEFAULT,
        help_text="カテゴリ",
        default="Uncategorized",
    )
    difficulty = models.ForeignKey(
        "Difficulty",
        on_delete=models.SET_DEFAULT,
        help_text="難易度",
        default="Easy",
    )
    is_open = models.BooleanField(help_text="公開中かどうか", default=True)
    created_at = models.DateTimeField(auto_now_add=True, help_text="作成日時")
    updated_at = models.DateTimeField(auto_now=True, help_text="更新日時")

    def __str__(self):
        return self.title

    class Meta:
        app_label = "ctf"
        verbose_name = verbose_name_plural = "問題"


class Category(models.Model, ExportModelOperationsMixin("category")):
    """CTF 問題カテゴリ"""

    name = models.CharField(max_length=255, help_text="カテゴリ名", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = "ctf"
        verbose_name = verbose_name_plural = "問題カテゴリ"


class Difficulty(models.Model, ExportModelOperationsMixin("difficulty")):
    """CTF 問題難易度"""

    level = models.PositiveSmallIntegerField(help_text="難易度レベル", unique=True)
    name = models.CharField(max_length=255, help_text="難易度名", unique=True)

    def __str__(self):
        return f"{self.level} - {self.name}"

    class Meta:
        app_label = "ctf"
        verbose_name = verbose_name_plural = "問題難易度"