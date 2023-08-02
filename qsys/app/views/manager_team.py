from django.urls import reverse
from django.views import defaults
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ctf.models.contest import Contest
from ctf.models.player import Player


@login_required
def manager_team(request):
    if request.method == "GET":
        contests = Contest.objects.all()
        if contests == 0:
            messages.info(request, "コンテストが開催されていません")
            return render(request, "app/manager_team.html")

        actives = Contest.get_active_contests()
        if actives.count() > 1:
            actives = actives.order_by("start_at")
        active = actives.first()

        if active is None:
            active = contests.first()

        ctx = {}
        ctx["all_contests"] = contests
        ctx["active_contest"] = active
        ctx["all_teams"] = active.teams.all()
        ctx["active_team"] = active.teams.all().first()

        if request.GET.get("contest_id"):
            c = get_object_or_404(Contest, pk=request.GET.get("contest_id"))
            ctx["active_contest"] = c

        if request.GET.get("team_id"):
            try:
                c = ctx["active_contest"]
                ctx["active_team"] = c.teams.get(pk=request.GET.get("team_id"))
            except Exception:
                return defaults.page_not_found(
                    request, None, template_name="http/404.html"
                )

        members = ctx.get("active_team").members.all()
        players = Player.objects.all().difference(members)

        players_team_set = []
        for player in players:
            if player.teams is None:
                players_team_set.append({
                    "player": player,
                    "team": None
                })
                continue

            teams = ctx["all_teams"]
            ts = player.teams.all()
            team = None
            for t in ts:
                if t in teams:
                    team = t
                    break
            players_team_set.append({
                "id": player.id,
                "name": player.name,
                "team": team
            })

        members_team_set = []
        for member in members:
            members_team_set.append({
                "id": member.id,
                "name": member.name,
                "team": ctx["active_team"]
            })

        ctx["team_members"] = members_team_set
        ctx["players"] = players_team_set

        return render(request, "app/manager_team.html", ctx)

    elif request.method == "POST":
        contest_id = request.GET.get("contest_id")
        team_id = request.GET.get("team_id")
        user_id = request.POST.get("user_id")
        contest = get_object_or_404(Contest, pk=contest_id)
        team = get_object_or_404(contest.teams.all(), pk=team_id)
        player = get_object_or_404(Player, pk=user_id)

        ctrl_type = request.POST.get("type")
        if ctrl_type == "add":
            team.members.add(player)
            team.save()
        elif ctrl_type == "remove":
            team.members.remove(player)
            team.save()

        return_params = "?contest_id=" + contest_id + "&team_id=" + team_id
        return redirect(reverse("manager_team") + return_params)

    return defaults.server_error(request, template_name="http/500.html")
