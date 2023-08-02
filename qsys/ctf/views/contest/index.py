from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from ctf.models.contest import Contest


@login_required
def contest_view(request: HttpRequest, contest_id: str):
    contest = get_object_or_404(Contest, id=contest_id)
    ctx = {"contest": contest}
    if not contest.is_open:
        if not request.user.is_admin:
            return redirect("ctf:index")
        messages.info(request, "このコンテストは非公開です")

    return render(request, "ctf/contest/home.html", ctx)
