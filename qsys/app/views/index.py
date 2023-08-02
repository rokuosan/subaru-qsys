from django.shortcuts import render

from ctf.models.contest import Contest


def index(request):
    ctx = {}

    contest = Contest.get_active_contests()
    if contest is not None:
        ctx["contest"] = contest

    return render(request, "app/index.html", ctx)
