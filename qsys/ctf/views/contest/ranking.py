from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from ctf.models.contest import Contest
from ctf.utils.contest_util import ContestUtils


@login_required
def ranking_view(request: HttpRequest, contest_id: str):
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    ctx = {"contest": contest}
    cu = ContestUtils(contest)

    # 公開設定
    fun = cu.get_page_protection(request)
    if fun is not None:
        return fun[0](*fun[1], **fun[2])

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
