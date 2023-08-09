from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ctf.models.contest import Contest
from ctf.utils.contest_util import ContestUtils


@login_required
def manager_team_view(request: HttpRequest):
    """チーム管理画面を表示するView"""
    if not request.user.is_admin:
        return redirect("ctf:index")
    ctx = {}
    contests = Contest.objects.all()
    if not contests.exists():
        messages.info(request, "コンテストが登録されていません")

    cid = request.GET.get("contest_id")
    selected_contest = get_object_or_404(Contest, id=cid) if cid else None
    if selected_contest is None:
        selected_contest = contests.first()

    cu = ContestUtils(selected_contest)
    players = cu.get_players()

    ctx["contests"] = contests
    ctx["selected_contest"] = selected_contest
    ctx["players"] = players
    return render(request, "ctf/manager/team.html", ctx)
