from django.urls import reverse
from django.views import defaults
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from app.models.ctf_information import CtfInformation
from app.models.team import CtfTeam


@login_required
def manager_team(request):
    if request.method == "GET":
        ctfs = CtfInformation.objects.all()
        if ctfs.count() == 0:
            messages.info(request, "CTFが開催されていません")
            return render(request, "app/manager_team.html")

        actives = ctfs.filter(is_active=True)
        if actives.count() > 1:
            actives = actives.order_by("start_at")
        active = actives.first()

        if active is None:
            active = ctfs.first()

        # teams = active.get_teams(ctf_id=active.ctf_id)
        teams = CtfTeam.objects.all()

        ctx = {}
        ctx["all_teams"] = teams
        ctx["all_ctfs"] = ctfs
        ctx["active_ctf"] = active
        ctx["active_team"] = teams.first()

        if request.GET.get("ctf_id"):
            try:
                c = ctfs.get(ctf_id=request.GET.get("ctf_id"))
                ctx["active_ctf"] = c
                # teams = c.get_teams(ctf_id=c.ctf_id)
                # ctx["all_teams"] = teams
            except CtfInformation.DoesNotExist:
                messages.warning(request, "指定されたCTFが見つかりませんでした")

        if request.GET.get("team_id"):
            try:
                tid = int(request.GET.get("team_id"))
                lst = list(filter(lambda t: t.team_id == tid, teams))
                ctx["active_team"] = lst.pop()
            except (CtfInformation.DoesNotExist, IndexError, ValueError):
                messages.warning(request, "指定されたチームが見つかりませんでした")

        team_members = []
        users = []
        if ctx.get("active_team"):
            tid = ctx["active_team"].team_id
            team_members = ctx["active_ctf"].participants.filter(team_id=tid)
            users = ctx["active_ctf"].participants.exclude(team_id=tid)

        ctx["team_members"] = team_members
        ctx["users"] = users

        return render(request, "app/manager_team.html", ctx)

    elif request.method == "POST":
        ctf_id = request.GET.get("ctf_id")
        team_id = request.GET.get("team_id")
        user_id = request.POST.get("user_id")
        ctf = CtfInformation.objects.get(ctf_id=ctf_id)
        team = CtfTeam.objects.get(team_id=team_id)
        user = ctf.participants.get(pk=user_id)

        ctrl_type = request.POST.get("type")
        if ctrl_type == "add":
            user.team = team
            user.save()
        elif ctrl_type == "remove":
            user.team = None
            user.save()

        return_params = "?ctf_id=" + ctf_id + "&team_id=" + team_id
        return redirect(reverse("manager_team") + return_params)

    return defaults.server_error(request, template_name="http/500.html")
