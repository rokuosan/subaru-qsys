from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ctf.models.contest import Contest
from ctf.utils.contest_util import ContestUtils
from ctf.models.player import Player


@login_required
def manager_team_view(request: HttpRequest, contest_id: str):
    """チーム管理画面を表示するView"""
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    if not request.user.is_admin:
        return redirect("ctf:home", contest_id=contest.id)
    ctx = {}
    contests = Contest.objects.all()
    if not contests.exists():
        messages.info(request, "コンテストが登録されていません")

    cu = ContestUtils(contest)
    players = cu.get_players(all=True)
    teams = contest.teams.all()

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
        return redirect(
            reverse("ctf:manager_team", args=[contest.id])
            + f"?{params.urlencode()}"
        )

    players = [p for p in players if p not in members]

    no_team = []
    on_team = []
    for p in players:
        t = cu.get_team_by_player(p)
        if t:
            on_team.append(p)
        else:
            no_team.append(p)

    ctx["contests"] = contests
    ctx["contest"] = contest
    ctx["players"] = [
        {
            "type": "未加入",
            "players": no_team,
        },
        {
            "type": "チーム加入済み",
            "players": on_team,
        },
    ]
    ctx["teams"] = teams
    ctx["selected_team"] = selected_team
    ctx["members"] = members

    return render(request, "ctf/contest/manager/team.html", ctx)


@login_required
def manager_team_create_view(request: HttpRequest, contest_id: str):
    contest = get_object_or_404(Contest, id=contest_id)
    cu = ContestUtils(contest)
    if not request.user.is_admin:
        return redirect("ctf:home", contest_id=contest.id)

    if request.method != "POST":
        return redirect("ctf:manager_team", contest_id=contest.id)

    name = request.POST.get("team_name")
    if not name:
        messages.error(request, "チーム名を入力してください")
        return redirect("ctf:manager_team", contest_id=contest.id)

    teams = contest.teams.all()
    if teams.filter(name=name).exists():
        messages.error(request, "そのチーム名は既に使用されています")
        return redirect("ctf:manager_team", contest_id=contest.id)

    team = cu.create_team(name)
    if team is None:
        messages.error(request, "チームの作成に失敗しました")
        return redirect("ctf:manager_team", contest_id=contest.id)

    messages.success(request, "チームを作成しました")
    return redirect("ctf:manager_team", contest_id=contest.id)
