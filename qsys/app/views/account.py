from app.models.history import CtfAnswerHistory
from app.models.ctf_information import CtfInformation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import render


@login_required
def account(request: HttpRequest):
    ctx = {}
    ctx["display"] = {
        "username": request.user.username,
        "answers": [],
        "point": 0,
        "ratio": 0,
    }

    # Get CTF
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
        "answers": answers,
        "point": point,
        "ratio": ratio,
    }

    return render(request, "app/account.html", ctx)
