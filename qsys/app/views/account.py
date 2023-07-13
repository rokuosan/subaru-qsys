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
        "team": '-',
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

    # Get Answers
    answers_original = CtfAnswerHistory.objects.filter(
        user=request.user, ctf=ctf
    )
    answers_original = answers_original.order_by("-answered_at")
    # Last newest 10 answers
    answers = answers_original[:10]

    # Your point
    point = 0
    correct_answers = answers_original.filter(is_correct=True)
    point = sum([answer.question.point for answer in correct_answers])

    # Answer ratio
    max = len(answers_original)
    corrects = len(correct_answers)
    if max == 0:
        ratio = 0
    else:
        ratio = round(corrects / max * 100, 2)

    ctx["display"] = {
        "username": request.user.username,
        "team": request.user.team,
        "answers": answers,
        "point": point,
        "ratio": ratio,
        "team_ratio": "-",
        "team_point": "-",
    }

    if request.user.team:
        teammate = ctf.participants.filter(team=request.user.team)
        scores = CtfScore.objects.filter(user__in=teammate, ctf=ctf)
        team_point = sum([score.point for score in scores])

        all_answers = CtfAnswerHistory.objects.filter(
            user__in=teammate, ctf=ctf
        )
        all_correct_answers = all_answers.filter(is_correct=True)

        all = len(all_answers)
        corrects = len(all_correct_answers)
        if all == 0:
            ratio = 0
        else:
            ratio = round(corrects / all * 100, 2)

        ctx["display"]["team_ratio"] = ratio
        ctx["display"]["team_point"] = team_point

    return render(request, "app/account.html", ctx)
