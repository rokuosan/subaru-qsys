from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from ctf.models.contest import Contest
from ctf.utils.contest_util import ContestUtils


@login_required
def contest_home_view(request: HttpRequest, contest_id: str):
    contest = get_object_or_404(Contest, id=contest_id)
    ctx = {"contest": contest}
    if not contest.is_open:
        if not request.user.is_admin:
            return redirect("ctf:index")
        messages.info(request, "このコンテストは非公開です")

    status_table = {
        "preparing": ("準備中", "info", "preparing"),
        "running": ("開催中", "success", "running"),
        "finished": ("終了", "danger", "finished"),
        "paused": ("一時停止中", "warning", "paused"),
    }
    ctx["status_table"] = [
        (s, status_table[s][0]) for s in status_table.keys()
    ]
    ctx["status"] = status_table[contest.status]
    ctx["is_open"] = contest.is_open

    cu = ContestUtils(contest)

    player_count = ("参加者数", len(cu.get_players()))
    team_count = ("チーム数", contest.teams.count())
    problem_count = ("登録問題数", contest.questions.count())
    duration = ("開催時間", contest.end_at - contest.start_at)

    ctx["contest_info"] = [
        duration,
        player_count,
        team_count,
        problem_count,
    ]

    return render(request, "ctf/contest/home.html", ctx)
