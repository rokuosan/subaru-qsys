from datetime import datetime
from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from .team import CtfTeam
from .app_user import AppUser
from .question import CtfQuestion


class CtfInformation(
    ExportModelOperationsMixin("ctf_information"), models.Model
):
    """CTF情報"""

    ctf_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, help_text="CTF名")
    description = models.TextField(help_text="CTF説明")
    start_at = models.DateTimeField(help_text="開始日時")
    end_at = models.DateTimeField(help_text="終了日時")

    questions = models.ManyToManyField(CtfQuestion, help_text="問題", blank=True)
    participants = models.ManyToManyField(AppUser, help_text="参加者", blank=True)

    is_active = models.BooleanField(default=False, help_text="CTF実施状況")
    is_paused = models.BooleanField(default=False, help_text="CTF一時停止状況")

    show_team_ranking = models.BooleanField(
        default=True, help_text="チームランキング(Team Ranking)を公開する"
    )

    show_player_ranking = models.BooleanField(
        default=True, help_text="プレイヤーランキング(Player Ranking)を公開する"
    )

    # CTFが開始しているかどうか
    @property
    def is_started(self):
        now = datetime.now(tz=self.start_at.tzinfo)
        return self.start_at <= now

    # CTFが終了しているかどうか
    @property
    def is_ended(self):
        now = datetime.now(tz=self.start_at.tzinfo)
        return self.end_at <= now

    class Meta:
        app_label = "app"
        verbose_name = verbose_name_plural = "CTF情報"

    def __str__(self):
        return self.name

    @staticmethod
    def get_teams(ctf_id: int) -> list[CtfTeam]:
        """CTF参加者のチームを取得

        Args:
            ctf_id (int): CTF ID

        Returns:
            List[CtfTeam]: チームのリスト
        """
        teams = []
        users = CtfInformation.objects.get(ctf_id=ctf_id).participants.all()
        for user in users:
            if not user.team:
                continue
            if user.team not in teams:
                teams.append(user.team)
        teams = sorted(teams, key=lambda x: (x.name, x.team_id))
        return teams
