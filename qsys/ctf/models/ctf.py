from django.utils import timezone

from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class CTF(models.Model, ExportModelOperationsMixin("ctf")):
    """CTF 開催情報\n
    Properties:\n
    - ctf_id -> : CTF ID\n
    - name -> str: CTF名\n
    - description -> str: 紹介文\n
    - start_at -> datetime: 開始日時\n
    - end_at -> datetime: 終了日時\n
    - status -> str: CTFの状態\n
    - is_team_ranking_public -> bool: チームランキング(Team Ranking)を公開する\n
    - is_player_ranking_public -> bool: プレイヤーランキング(Player Ranking)を公開する\n

    Methods:\n
    - is_running -> bool: CTFが開催中かどうかを返す\n
    - is_paused -> bool: CTFが一時停止中かどうかを返す\n
    - is_finished -> bool: CTFが終了しているかどうかを返す\n
    - is_preparing -> bool: CTFが準備中かどうかを返す\n
    - is_open -> bool: CTFが実施中かどうかを返す\n
    - is_over -> bool: CTFが開催期間を過ぎているかどうかを返す\n
    - is_started_on_time -> bool: 開催期間を基準にCTFが開催しているかどうかを返す\n
    """

    name = models.CharField(max_length=255, help_text="CTF名")
    description = models.TextField(help_text="紹介文", blank=True, default="")

    start_at = models.DateTimeField(
        help_text="開始日時", default=timezone.now().replace(microsecond=0)
    )
    end_at = models.DateTimeField(
        help_text="終了日時", default=timezone.now()+timezone.timedelta(hours=2)
    )

    status = models.CharField(
        max_length=255,
        help_text="CTFの状態",
        choices=(
            ("preparing", "準備中"),
            ("running", "開催中"),
            ("paused", "一時停止中"),
            ("finished", "終了"),
        ),
        default="preparing",
    )

    is_team_ranking_public = models.BooleanField(
        default=True, help_text="チームランキング(Team Ranking)を公開する"
    )

    is_player_ranking_public = models.BooleanField(
        default=False, help_text="プレイヤーランキング(Player Ranking)を公開する"
    )

    def __str__(self):
        return self.name

    class Meta:
        app_label = "ctf"
        verbose_name = "CTF大会情報"
        verbose_name_plural = "CTF大会情報"
        ordering = ["-start_at"]

    def is_running(self):
        """CTFが開催中かどうかを返す"""
        return self.status == "running"

    def is_paused(self):
        """CTFが一時停止中かどうかを返す"""
        return self.status == "paused"

    def is_finished(self):
        """CTFが終了しているかどうかを返す"""
        return self.status == "finished"

    def is_preparing(self):
        """CTFが準備中かどうかを返す"""
        return self.status == "preparing"

    def is_open(self):
        """CTFが実施中かどうかを返す"""
        return self.is_running() or self.is_paused()

    def is_over(self):
        """CTFが開催期間を過ぎているかどうかを返す"""
        return self.end_at < timezone.now()

    def is_started_on_time(self):
        """開催期間を基準にCTFが開催しているかどうかを返す"""
        return self.start_at < timezone.now()

