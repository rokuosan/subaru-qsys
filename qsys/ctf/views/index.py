from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from ctf.models.contest import Contest
from ctf.utils.contest_util import ContestUtils


@login_required
def index_view(request: HttpRequest):
    ctx = {}

    try:
        player = request.user.player
    except Exception:
        return redirect("index")

    contests = Contest.objects.all()
    ctx["contests"] = contests

    joined_contests = []
    for contest in contests:
        cu = ContestUtils(contest)
        if player in cu.get_players():
            joined_contests.append(contest)

    opened_contests = []
    closed_contests = []
    for contest in contests:
        if contest.is_open:
            opened_contests.append(contest)
        else:
            closed_contests.append(contest)

    ctx["opened_contests"] = opened_contests
    if request.user.is_admin:
        ctx["closed_contests"] = closed_contests

    return render(request, "ctf/index.html", ctx)
