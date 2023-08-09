from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from ctf.models.contest import Contest
from qsys.ctf.utils.contest_util import ContestUtils


@login_required
def ranking_view(request: HttpRequest, contest_id: str):
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    ctx = {"contest": contest}
    cu = ContestUtils(contest)

    # 公開設定
    if not contest.is_open:
        messages.info(request, "このコンテストは非公開です")
        if not request.user.is_admin:
            return redirect("ctf:index")
    if contest.status != Contest.Status.RUNNING:
        messages.info(request, "このコンテストは開催中ではありません")
        if not request.user.is_admin:
            return redirect("ctf:index")

    # 参加者情報
    try:
        player = request.user.player
    except Exception:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")
    team = contest.get_team_by_player(player)
    ctx["user"] = request.user
    ctx["player"] = player
    ctx["team"] = team

    # ランキング
    if contest.is_player_ranking_public or request.user.is_admin:
        ctx["player_ranking"] = cu.make_player_ranking()
    if contest.is_team_ranking_public or request.user.is_admin:
        ctx["team_ranking"] = cu.make_team_ranking()

    return render(request, "ctf/contest/ranking.html", ctx)
