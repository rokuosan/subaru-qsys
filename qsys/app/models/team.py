from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class CtfTeam(ExportModelOperationsMixin('ctf_team'), models.Model):
    """CTFチーム"""
    team_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, help_text='チーム名')

    is_admin = models.BooleanField(default=False, help_text='管理者チーム')

    class Meta:
        app_label = 'app'
        verbose_name = verbose_name_plural = 'チーム'

    def __str__(self):
        return self.name
