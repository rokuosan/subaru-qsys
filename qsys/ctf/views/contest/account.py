from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from ctf.models.contest import Contest
from ctf.models.history import History
from ctf.utils.contest_util import ContestUtils


@login_required
def account_view(request: HttpRequest, contest_id: str):
    contest: Contest = get_object_or_404(Contest, id=contest_id)
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

    player = ctx["player"]
    team = ctx["team"]

    # 回答履歴の取得
    history = History.objects.filter(player=player, contest=contest).order_by(
        "-created_at"
    )
    for h in history:
        h.reason = History.ResultType.get_name(h.result)
    ctx["history"] = history

    # 点数と正答率の計算
    p_point = History.get_player_point(contest, player)
    p_acc = History.get_player_accuracy(contest, player)
    t_point = History.get_team_point(contest, team)
    t_acc = History.get_team_accuracy(contest, team)

    ctx["player_point"] = p_point
    ctx["player_accuracy"] = round(p_acc, 2)
    ctx["team_point"] = t_point
    ctx["team_accuracy"] = round(t_acc, 2)

    return render(request, "ctf/contest/account.html", ctx)
