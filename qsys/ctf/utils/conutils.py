from ctf.models.contest import Contest
from ctf.models.team import Team
from ctf.models.player import Player
from ctf.models.history import History


class ConUtils:
    def __init__(self, contest: Contest) -> None:
        self.contest = contest

    def get_team_by_player(self, player) -> Team | None:
        """プレイヤーが所属するチームを返す"""
        try:
            return self.contest.teams.get(members__id=player.id)
        except Exception:
            return None

    def get_players(self):
        """コンテストに参加しているプレイヤーを取得する"""
        teams = self.contest.teams.all()

        players = []
        for team in teams:
            players += team.members.all()

        return players

    def make_player_ranking(self) -> list[Player]:
        """プレイヤーのランキングを作成する。player.rankに順位が入る"""
        players = self.get_players()

        # それぞれに点数をつける
        for player in players:
            player.point = History.get_player_point(self.contest, player)

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
        """チームのランキングを作成する。team.rankに順位が入る"""
        teams = list(self.contest.teams.all())

        # それぞれに点数をつける
        for team in teams:
            team.point = History.get_team_point(self.contest, team)

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
