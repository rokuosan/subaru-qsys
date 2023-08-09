from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from ctf.models.contest import Contest
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
    history = cu.get_player_history(player)
    ctx["history"] = history

    # 点数と正答率の計算
    p_point = cu.get_point(player)
    p_acc = cu.get_accuracy(player)
    t_point = "-"
    t_acc = "-"
    if team is not None:
        t_point = cu.get_point(team)
        t_acc = cu.get_accuracy(team)

    ctx["player_point"] = p_point
    ctx["player_accuracy"] = p_acc
    ctx["team_point"] = t_point
    ctx["team_accuracy"] = t_acc

    return render(request, "ctf/contest/account.html", ctx)
