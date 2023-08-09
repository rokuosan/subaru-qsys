from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ctf.models.contest import Contest
from ctf.utils.contest_util import ContestUtils
from ctf.models.player import Player


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
    players = cu.get_players(all=True)
    teams = selected_contest.teams.all()

    for p in players:
        p.team = cu.get_team_by_player(p)

    tid = request.GET.get("team_id")
    selected_team = get_object_or_404(teams, id=tid) if tid else None
    if selected_team is None:
        selected_team = teams.first()

    members = selected_team.members.all()
    for m in members:
        m.team = selected_team

    if request.method == "POST":
        player_id = request.POST.get("player_id")
        player = get_object_or_404(Player, id=player_id)
        ctrl_type = request.POST.get("type")
        if ctrl_type == "add":
            before = cu.get_team_by_player(player)
            if before is not None:
                before.members.remove(player)
                before.save()
            selected_team.members.add(player)
            selected_team.save()
        elif ctrl_type == "remove":
            selected_team.members.remove(player)
            selected_team.save()

        params = request.GET.copy()
        return redirect(reverse("ctf:manager_team")+f"?{params.urlencode()}")

    players = [p for p in players if p not in members]

    ctx["contests"] = contests
    ctx["selected_contest"] = selected_contest
    ctx["players"] = players
    ctx["teams"] = teams
    ctx["selected_team"] = selected_team
    ctx["members"] = members

    return render(request, "ctf/manager/team.html", ctx)
