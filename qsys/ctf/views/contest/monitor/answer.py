from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from ctf.models.contest import Contest


@login_required
def answer_view(request: HttpRequest, contest_id: str):
    contest = get_object_or_404(Contest, pk=contest_id)
    ctx = {"contest": contest}
    return render(request, 'ctf/contest/monitor/answer.html', ctx)
