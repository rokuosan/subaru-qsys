from app.models.history import CtfAnswerHistory
from app.models.ctf_information import CtfInformation
from app.models.score import CtfScore
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render


@login_required
def account(request: HttpRequest):
    ctx = {}
    ctx["display"] = {
        "username": request.user.username,
        "team": "-",
        "answers": [],
        "point": 0,
        "ratio": 0,
        "team_ratio": "-",
        "team_point": "-",
    }

    # Get CTF
    ctf = None
    ctfs = CtfInformation.objects.filter(is_active=True)
    if not ctfs:
        messages.warning(request, "CTFが開催されていません")
        return render(request, "app/account.html", ctx)
    for c in ctfs:
        if request.user in c.participants.all():
            ctf = c
            break

    if ctf is None:
        messages.warning(request, "CTFに参加していません")
        return render(request, "app/account.html", ctx)

    # Get last newest 10 Answers
    answers = CtfAnswerHistory.objects.filter(
        user=request.user, ctf=ctf
    ).order_by("-answered_at")[:10]

    # Your point
    point = CtfAnswerHistory.get_user_point(request.user, ctf)

    # Answer ratio
    ac = CtfAnswerHistory.get_user_accuracy(request.user, ctf) * 100

    ctx["display"] = {
        "username": request.user.username,
        "team": request.user.team,
        "answers": answers,
        "point": point,
        "ratio": round(ac, 2),
        "team_ratio": "-",
        "team_point": "-",
    }

    if request.user.team:
        tac = CtfAnswerHistory.get_team_accuracy(request.user.team, ctf) * 100
        tpt = CtfAnswerHistory.get_team_point(request.user.team, ctf)

        ctx["display"]["team_ratio"] = round(tac, 2)
        ctx["display"]["team_point"] = tpt

    return render(request, "app/account.html", ctx)
