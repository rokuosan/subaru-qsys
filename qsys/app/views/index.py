from django.shortcuts import render
from django.db.models import Q

from ctf.models.contest import Contest


def index(request):
    ctx = {}

    contest = Contest.objects.filter(
        Q(status="running") | Q(status="paused")
    ).first()
    if contest is not None:
        ctx["contest"] = contest

    return render(request, "app/index.html", ctx)
