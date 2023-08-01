from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class Team(models.Model, ExportModelOperationsMixin("team")):
    """CTF チーム"""
    name = models.CharField(max_length=255, help_text="チーム名", unique=True)

    members = models.ManyToManyField(
        "AppUser", help_text="チームメンバー", related_name="teams", blank=True
    )

    class Meta:
        app_label = "ctf"
        verbose_name = "チーム"
        verbose_name_plural = "チーム"

    def __str__(self):
        return self.name
