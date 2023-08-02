from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ctf.models.contest import Contest


@login_required
def manager_contest_view(request: HttpRequest):
    if not request.user.is_admin:
        return redirect("ctf:index")

    if request.method == "POST":
        contest_id = request.POST.get("contest_id")
        contest = get_object_or_404(Contest, id=contest_id)

        status = request.POST.get("status")
        contest.status = status

        is_open = request.POST.get("is_open")
        contest.is_open = is_open == "True"

        contest.save()
        return redirect("ctf:manager_contest")

    open_contests = Contest.objects.filter(is_open=True)
    closed_contests = Contest.objects.filter(is_open=False)

    ctx = {
        "all_contests": [
            {
                "name": "Public Contests",
                "contests": open_contests,
            },
            {
                "name": "Private Contests",
                "contests": closed_contests,
            },
        ]
    }

    return render(request, "ctf/manager/contest.html", ctx)
