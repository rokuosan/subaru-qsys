from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class Question(models.Model, ExportModelOperationsMixin("question")):
    """CTF 問題"""
    pass


class Category(models.Model, ExportModelOperationsMixin("category")):
    """CTF 問題カテゴリ"""
    pass


class Difficulty(models.Model, ExportModelOperationsMixin("difficulty")):
    """CTF 問題難易度"""
    pass
