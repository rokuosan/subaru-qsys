from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class History(models.Model, ExportModelOperationsMixin("history")):
    """CTF 回答履歴"""
    pass
