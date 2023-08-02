from django.shortcuts import render

from ctf.models.contest import Contest


def index(request):
    ctx = {}

    contest = Contest.objects.filter(status="running" or "preparing").first()
    if contest is not None:
        contest.name = contest.display_name or contest.id
        ctx["contest"] = contest

    return render(request, "app/index.html", ctx)
