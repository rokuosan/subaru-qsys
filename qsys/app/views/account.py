from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app.models.history import CtfAnswerHistory


@login_required
def account(request: HttpRequest):
    ctx = {}

    # Get Answers
    answers_original = CtfAnswerHistory.objects.filter(user=request.user)
    answers_original = answers_original.order_by("-answered_at")
    # Last newest 10 answers
    answers = answers_original[:10]

    # Your point
    point = 0
    point = sum([answer.question.point for answer in answers_original])

    # Answer ratio
    length = len(answers_original)
    if length == 0:
        ratio = 0
    else:
        ratio = point / length

    ctx["display"] = {
        "username": request.user.username,
        "answers": answers,
        "point": point,
        "ratio": ratio,
    }

    return render(request, "app/account.html", ctx)
