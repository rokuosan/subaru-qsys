from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ctf.models.contest import Contest
from ctf.utils.contest_util import ContestUtils


@login_required
def answer_view(request: HttpRequest, contest_id: str):
    contest = get_object_or_404(Contest, pk=contest_id)
    cu = ContestUtils(contest)

    # 公開設定
    fun = cu.get_page_protection(request)
    if fun is not None:
        return fun[0](*fun[1], **fun[2])

    # コンテキストの初期化
    ctx = cu.set_initial_context(request)
    if ctx["player"] is None:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")
    ctx["total"] = 0

    player = ctx["player"]
    team = ctx["team"]

    # 回答履歴の取得
    history = cu.get_history().order_by("-created_at")
    ctx["history"] = history

    # 全プレイヤーを取得
    players = cu.get_players()
    ctx["players"] = players

    # 全チームを取得
    teams = contest.teams.all()
    ctx["teams"] = teams

    # パラメータ解析
    player_id = request.GET.get("player_id")
    if player_id is not None:
        if player_id == "all":
            ctx["history"] = history
        else:
            player = get_object_or_404(cu.get_players(all=True), pk=player_id)
            history = history.filter(player=player)
            ctx["history"] = history
            ctx["selected_player"] = player

    team_id = request.GET.get("team_id")
    if team_id is not None:
        if team_id == "all":
            ctx["history"] = history
        else:
            team = get_object_or_404(teams, pk=team_id)
            history = ctx["history"].filter(team=team)
            ctx["history"] = history
            ctx["selected_team"] = team

    ctx["total"] = len(ctx["history"])
    return render(request, 'ctf/contest/monitor/answer.html', ctx)
