from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def stats_view(request: HttpRequest, contest_id: str):
    ctx = {}
    return render(request, 'ctf/contest/monitor/stats.html', ctx)
