from typing import Callable
from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import redirect
from app.models.app_user import AppUser
from ctf.models.contest import Contest
from ctf.models.team import Team
from ctf.models.player import Player
from ctf.models.history import History
from ctf.models.question import Question


class ContestUtils:
    """コンテストに関するユーティリティクラス"""

    def __init__(self, contest: Contest) -> None:
        self.contest = contest

    def get_page_protection(
        self, request: HttpRequest
    ) -> (Callable[[], None] | None, list, dict):
        if not self.contest.is_open:
            messages.info(request, "このコンテストは非公開です")
            if not request.user.is_admin:
                return (redirect, ["ctf:index"], {})

        if self.contest.status != Contest.Status.RUNNING:
            messages.info(request, "このコンテストは開催中ではありません")
            if not request.user.is_admin:
                return (
                    redirect,
                    ["ctf:home"],
                    {"contest_id": self.contest.id},
                )

        return None

    def set_initial_context(self, request: HttpRequest) -> dict:
        ctx = {"contest": self.contest}
        player = self.get_player(request.user)
        team = self.get_team_by_player(player)
        ctx["player"] = player
        ctx["team"] = team

        return ctx

    def get_player(self, user: AppUser) -> Player | None:
        try:
            return user.player
        except Exception:
            return None

    def get_history(self) -> list[History]:
        return History.objects.filter(contest=self.contest)

    def get_team_by_player(self, player) -> Team | None:
        """プレイヤーが所属するチームを返す

        Args:
            player (Player): チームを取得したいプレイヤー

        Returns:
            Team | None: 所属しているチーム。所属していない場合はNone
        """
        try:
            return self.contest.teams.get(members__id=player.id)
        except Exception:
            return None

    def get_players(self, all: bool = False) -> list[Player]:
        """コンテストに参加しているプレイヤーをリストで返す

        Returns:
            list[Player]: 参加しているプレイヤー
            all (bool): Trueの場合は全プレイヤーを返す
        """
        if all:
            return Player.objects.all()

        teams = self.contest.teams.all()

        players = []
        for team in teams:
            players += team.members.all()

        return players

    def get_point(self, target: Team | Player) -> int:
        """プレイヤーまたはチームの獲得ポイントを返す

        Args:
            target (Team | Player): ポイントを取得したいプレイヤーまたはチーム

        Returns:
            int: 獲得ポイント
        """
        if isinstance(target, Team):
            history = History.objects.filter(
                contest=self.contest,
                team=target,
                is_correct=True,
            )
            return sum([h.point for h in history])
        elif isinstance(target, Player):
            history = History.objects.filter(
                contest=self.contest,
                player=target,
                is_correct=True,
            )
            return sum([h.point for h in history])
        else:
            raise TypeError

    def get_accuracy(self, target: Team | Player) -> float:
        """プレイヤーまたはチームの正答率を返す

        Args:
            target (Team | Player): 正答率を取得したいプレイヤーまたはチーム

        Returns:
            float: 正答率。小数点以下2桁までの百分率の値で返す
        """
        if isinstance(target, Player):
            history = History.objects.filter(
                contest=self.contest,
                player=target,
            )
            if history.count() == 0:
                return 0
            correct = history.filter(is_correct=True).count()

            return round(correct / history.count() * 100, 2)
        elif isinstance(target, Team):
            history = History.objects.filter(
                contest=self.contest,
                team=target,
            )
            if history.count() == 0:
                return 0
            correct = history.filter(is_correct=True).count()

            return round(correct / history.count() * 100, 2)
        else:
            raise TypeError

    def get_player_history(self, player: Player) -> list[History]:
        """プレイヤーの回答履歴を返す

        Args:
            player (Player): 回答履歴を取得したいプレイヤー

        Returns:
            list[History]: 回答履歴
        """
        history = list(
            History.objects.filter(
                contest=self.contest,
                player=player,
            ).order_by("-created_at")
        )
        for h in history:
            h.reason = History.ResultType.get_name(h.result)
        return history

    def get_solved_questions(self, target: Player | Team) -> list[Question]:
        """解答した問題を返す

        Args:
            target (Player | Team): プレイヤーもしくはチーム

        Returns:
            list[Question]: 解答した問題
        """
        if isinstance(target, Player):
            history = History.objects.filter(
                contest=self.contest,
                player=target,
                is_correct=True,
            )
            return [h.question for h in history]
        elif isinstance(target, Team):
            history = History.objects.filter(
                contest=self.contest,
                team=target,
                is_correct=True,
            )
            return [h.question for h in history]
        else:
            raise TypeError

    def get_question_solved_count(self, question) -> int:
        """指定した問題が解かれた回数を返す

        Args:
            question (Question): 解かれた回数を取得したい問題

        Returns:
            int: 解かれた回数
        """
        history = History.objects.filter(
            contest=self.contest,
            question=question,
            is_correct=True,
        )
        return history.count()

    def get_question_solved_rate(self, question) -> float:
        """指定した問題の正答率を返す

        Args:
            question (Question): 正答率を取得したい問題

        Returns:
            float: 正答率。小数点以下2桁までの百分率の値で返す
        """
        history = History.objects.filter(
            contest=self.contest,
            question=question,
        )
        if history.count() == 0:
            return 0
        correct = history.filter(is_correct=True).count()

        return round(correct / history.count() * 100, 2)

    def get_questions_with_statistics(self) -> list[dict]:
        """問題の統計情報を付与したリストを返す

        solved_count: 解かれた回数\n
        solved_rate: 正答率

        Returns:
            list[dict]: 統計情報付き問題リスト
        """
        questions = self.contest.questions.all()

        for question in questions:
            question.solved_count = self.get_question_solved_count(question)
            question.solved_rate = self.get_question_solved_rate(question)

        return questions

    def make_question_solved_ranking(self) -> list[dict]:
        """解答された回数の多い問題のランキングを返す

        Returns:
            list[dict]: ランキングつき問題リスト
        """
        questions = self.contest.questions.all()

        # それぞれに解かれた回数をつける
        for question in questions:
            question.solved_count = self.get_question_solved_count(question)

        # 順位をつけるが、同点の場合は同順位とする
        questions = sorted(
            questions, key=lambda x: x.solved_count, reverse=True
        )
        for i, question in enumerate(questions):
            if i == 0:
                question.rank = 1
            else:
                if question.solved_count == questions[i - 1].solved_count:
                    question.rank = questions[i - 1].rank
                else:
                    question.rank = i + 1

        return questions

    def make_player_ranking(self) -> list[Player]:
        """プレイヤーのランキングを作成する。
        player.rankに順位が格納されます。

        Returns:
            list[Player]: ランキングつきプレイヤーリスト
        """
        players = self.get_players()

        # それぞれに点数をつける
        for player in players:
            player.point = self.get_point(player)

        # 順位をつけるが、同点の場合は同順位とする
        players = sorted(players, key=lambda x: x.point, reverse=True)
        for i, player in enumerate(players):
            if i == 0:
                player.rank = 1
            else:
                if player.point == players[i - 1].point:
                    player.rank = players[i - 1].rank
                else:
                    player.rank = i + 1

        return players

    def make_team_ranking(self) -> list[Team]:
        """チームのランキングを作成する。team.rankに順位が入る

        Returns:
            list[Team]: ランキングつきチームリスト
        """
        teams = list(self.contest.teams.all())

        # それぞれに点数をつける
        for team in teams:
            team.point = self.get_point(team)

        # 順位をつけるが、同点の場合は同順位とする
        teams = sorted(teams, key=lambda x: x.point, reverse=True)
        for i, team in enumerate(teams):
            if i == 0:
                team.rank = 1
            else:
                if team.point == teams[i - 1].point:
                    team.rank = teams[i - 1].rank
                else:
                    team.rank = i + 1

        return teams

    def make_player_accuracy_ranking(self):
        """プレイヤーの正答率ランキングを作成する。
        player.accuracyに正答率が格納されます。

        Returns:
            list[Player]: ランキングつきプレイヤーリスト
        """
        players = self.get_players()

        # それぞれに正答率をつける
        for player in players:
            player.accuracy = self.get_accuracy(player)

        # 順位をつけるが、同点の場合は同順位とする
        players = sorted(players, key=lambda x: x.accuracy, reverse=True)
        for i, player in enumerate(players):
            if i == 0:
                player.rank = 1
            else:
                if player.accuracy == players[i - 1].accuracy:
                    player.rank = players[i - 1].rank
                else:
                    player.rank = i + 1

        return players

    def make_team_accuracy_ranking(self):
        """チームの正答率ランキングを作成する。
        team.accuracyに正答率が格納されます。

        Returns:
            list[Team]: ランキングつきチームリスト
        """
        teams = self.contest.teams.all()

        # それぞれに正答率をつける
        for team in teams:
            team.accuracy = self.get_accuracy(team)

        # 順位をつけるが、同点の場合は同順位とする
        teams = sorted(teams, key=lambda x: x.accuracy, reverse=True)
        for i, team in enumerate(teams):
            if i == 0:
                team.rank = 1
            else:
                if team.accuracy == teams[i - 1].accuracy:
                    team.rank = teams[i - 1].rank
                else:
                    team.rank = i + 1

        return teams

    def get_user(self, user_id: int) -> AppUser:
        """ユーザーIDからユーザーを取得する

        Args:
            user_id (int): ユーザーID

        Returns:
            User: ユーザー
        """
        try:
            return AppUser.objects.get(id=user_id)
        except AppUser.DoesNotExist:
            return None

    def get_users(self) -> AppUser:
        """ユーザーを全て取得する

        Returns:
            list[User]: ユーザーリスト
        """
        return AppUser.objects.all()

    def create_player(self, user: AppUser, name: str) -> Player:
        """プレイヤーを作成する

        Args:
            user_id (int): ユーザーID
            name (str): プレイヤー名

        Returns:
            Player: 作成したプレイヤー
        """
        try:
            player = Player.objects.create(
                user=user,
                name=name,
            )
            return player
        except Exception as e:
            print(e)
            return None

    def create_user(
        self, username: str, password: str, is_admin: bool = False
    ) -> AppUser:
        """ユーザーを作成する

        Args:
            username (str): ユーザー名
            password (str): パスワード

        Returns:
            User: 作成したユーザー
        """
        try:
            user = AppUser(
                username=username,
                is_admin=is_admin,
            )
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(e)
            return None

    def create_users(self, users: list[str]) -> list[tuple[str, str]]:
        """ユーザーを作成する

        Args:
            users (list[str]): ユーザー名のリスト

        Returns:
            list[tuple[str, str]]: 作成したユーザーとパスワードのタプルのリスト
        """
        pws = []
        for user in users:
            if user == "":
                continue
            if AppUser.objects.filter(username=user).exists():
                continue
            password = AppUser.objects.make_random_password()
            res = self.create_user(user, password)
            if res:
                pws.append((user, password))

        return pws
