from django.db import models
from django_prometheus.models import ExportModelOperationsMixin

from .app_user import AppUser
from .ctf_information import CtfInformation
from .question import CtfQuestion
from .team import CtfTeam


class CtfAnswerHistory(
    ExportModelOperationsMixin("ctf_answer_history"), models.Model
):
    """CTF問題回答履歴"""

    history_id = models.BigAutoField(primary_key=True)
    question = models.ForeignKey(CtfQuestion, models.CASCADE)
    user = models.ForeignKey(AppUser, models.CASCADE)
    team = models.ForeignKey(CtfTeam, models.CASCADE, null=True, blank=True)
    ctf = models.ForeignKey(
        CtfInformation,
        models.CASCADE,
        related_name="answer_history",
        null=True,
    )

    content = models.CharField(max_length=1023, help_text="回答内容")
    is_correct = models.BooleanField(default=False, help_text="正解フラグ")

    answered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = verbose_name_plural = "CTF問題回答履歴"
        app_label = "app"

    def __str__(self):
        return f"{self.answered_at}, {self.user}, {self.question}"

    @staticmethod
    def get_user_accuracy(user: AppUser, ctf: CtfInformation) -> float:
        """プレイヤーの正答率を取得

        Args:
            user (AppUser): 正答率を計算したいユーザー\n
            ctf (CtfInformation): 計算対象のCTF

        Returns:
            float: 正答率(0.0 ~ 1.0)
        """
        answered = CtfAnswerHistory.objects.filter(user=user, ctf=ctf).count()
        correct = CtfAnswerHistory.objects.filter(
            user=user, ctf=ctf, is_correct=True
        ).count()
        if answered == 0:
            return 0
        return correct / answered

    @staticmethod
    def get_team_accuracy(team: CtfTeam, ctf: CtfInformation) -> float:
        """チームの正答率を取得

        Args:
            team (CtfTeam): 正答率を計算したいチーム\n
            ctf (CtfInformation): 計算対象のCTF

        Returns:
            float: 正答率(0.0 ~ 1.0)
        """
        answered = CtfAnswerHistory.objects.filter(team=team, ctf=ctf).count()
        correct = CtfAnswerHistory.objects.filter(
            team=team, ctf=ctf, is_correct=True
        ).count()
        if answered == 0:
            return 0
        return correct / answered

    @staticmethod
    def get_user_point(user: AppUser, ctf: CtfInformation) -> int:
        """プレイヤーの獲得ポイントを取得

        Args:
            user (AppUser): 獲得ポイントを計算したいユーザー\n
            ctf (CtfInformation): 計算対象のCTF

        Returns:
            int: 獲得ポイント
        """
        answers = CtfAnswerHistory.objects.filter(user=user, ctf=ctf)
        point = 0
        point = sum([a.question.point for a in answers if a.is_correct])
        return point

    @staticmethod
    def get_team_point(team: CtfTeam, ctf: CtfInformation) -> int:
        """チームの獲得ポイントを取得

        Args:
            team (CtfTeam): 獲得ポイントを計算したいチーム\n
            ctf (CtfInformation): 計算対象のCTF

        Returns:
            int: 獲得ポイント
        """
        answers = CtfAnswerHistory.objects.filter(team=team, ctf=ctf)
        point = 0
        point = sum([a.question.point for a in answers if a.is_correct])
        return point
