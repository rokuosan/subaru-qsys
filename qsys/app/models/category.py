from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class CtfQuestionCategory(ExportModelOperationsMixin('ctf_question_category'), models.Model):
    """CTF問題カテゴリ"""
    category_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        app_label = 'app'
        verbose_name = verbose_name_plural = 'カテゴリ'

    def __str__(self):
        return self.category_name
