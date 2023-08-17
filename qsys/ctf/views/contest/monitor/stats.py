from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ctf.models.contest import Contest
from ctf.utils.contest_util import ContestUtils


@login_required
def stats_view(request: HttpRequest, contest_id: str):
    contest = get_object_or_404(Contest, pk=contest_id)
    cu = ContestUtils(contest)

    # 公開設定
    fun = cu.get_page_protection(request)
    if fun is not None:
        return fun[0](*fun[1], **fun[2])

    # 参加者情報
    ctx = cu.set_initial_context(request)
    if ctx["player"] is None:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")

    # 人気な問題
    qs = cu.get_questions_with_statistics()
    qs = sorted(qs, key=lambda q: q.solved_count, reverse=True)[:10]

    # ランキング
    ctx["player_ranking"] = cu.make_player_ranking()[:10]
    ctx["team_ranking"] = cu.make_team_ranking()
    ctx["popular_questions"] = qs
    ctx["player_accuracy_ranking"] = cu.make_player_accuracy_ranking()[:10]
    ctx["team_accuracy_ranking"] = cu.make_team_accuracy_ranking()

    return render(request, "ctf/contest/monitor/stats.html", ctx)
