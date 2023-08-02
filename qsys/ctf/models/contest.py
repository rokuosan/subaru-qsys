from django.utils import timezone
from django.core.validators import RegexValidator
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin


class Contest(models.Model, ExportModelOperationsMixin("ctf")):
    """CTF 開催情報\n
    Properties:\n
    - id -> : コンテストID\n
    - name -> str: コンテスト名\n
    - description -> str: 紹介文\n
    - start_at -> datetime: 開始日時\n
    - end_at -> datetime: 終了日時\n
    - status -> str: CTFの状態\n
    - is_team_ranking_public -> bool: チームランキング(Team Ranking)を公開する\n
    - is_player_ranking_public -> bool: プレイヤーランキング(Player Ranking)を公開する\n

    Methods:\n
    - is_running -> bool: コンテストが開催中かどうかを返す\n
    - is_paused -> bool: コンテストが一時停止中かどうかを返す\n
    - is_finished -> bool: コンテストが終了しているかどうかを返す\n
    - is_preparing -> bool: コンテストが準備中かどうかを返す\n
    - is_open -> bool: コンテストが実施中かどうかを返す\n
    - is_over -> bool: コンテストが開催期間を過ぎているかどうかを返す\n
    - is_started_on_time -> bool: 開催期間を基準にコンテストが開催しているかどうかを返す\n
    """

    id = models.CharField(
        max_length=255,
        help_text="コンテストID",
        primary_key=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9_-]{4,}$",
                message="IDは半角英数字とハイフン(-)、アンダースコア(_)のみ使用でき、4文字以上である必要があります。",
            ),
        ],
    )
    display_name = models.CharField(
        max_length=255, help_text="コンテスト名", null=True, blank=True
    )
    description = models.TextField(help_text="紹介文", blank=True, default="")

    start_at = models.DateTimeField(help_text="開始日時", default=timezone.now)
    end_at = models.DateTimeField(help_text="終了日時", default=timezone.now)

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
        if self.display_name:
            return self.display_name
        return self.id

    class Meta:
        app_label = "ctf"
        verbose_name = "コンテスト"
        verbose_name_plural = "コンテスト"
        ordering = ["-start_at"]

    class Status:
        """コンテストの状態を表す"""

        PREPARING = "preparing"
        RUNNING = "running"
        PAUSED = "paused"
        FINISHED = "finished"

    def set_status(self, status: Status):
        """コンテストの状態を設定する"""
        self.status = status
        self.save()

    @property
    def is_running(self):
        """コンテストが開催中かどうかを返す"""
        return self.status == "running"

    @property
    def is_paused(self):
        """コンテストが一時停止中かどうかを返す"""
        return self.status == "paused"

    @property
    def is_finished(self):
        """コンテストが終了しているかどうかを返す"""
        return self.status == "finished"

    @property
    def is_preparing(self):
        """コンテストが準備中かどうかを返す"""
        return self.status == "preparing"

    @property
    def is_open(self):
        """コンテストが実施中かどうかを返す"""
        return self.is_running() or self.is_paused()

    @property
    def is_over(self):
        """コンテストが開催期間を過ぎているかどうかを返す"""
        return self.end_at < timezone.now()

    @property
    def is_started_on_time(self):
        """開催期間を基準にコンテストが開催しているかどうかを返す"""
        return self.start_at < timezone.now()