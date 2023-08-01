from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class Scoreboard(models.Model, ExportModelOperationsMixin("scoreboard")):
    """CTF スコアボード"""
    pass
