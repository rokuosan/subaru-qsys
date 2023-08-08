from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from ctf.models.contest import Contest
from ctf.models.history import History


@login_required
def account_view(request: HttpRequest, contest_id: str):
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    ctx = {"contest": contest}

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
