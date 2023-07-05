from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from app.models.history import CtfAnswerHistory


@login_required
def account(request: HttpRequest):
    ctx = {}

    # Get Answers
    answers = CtfAnswerHistory.objects.filter(user=request.user)
    # Last newest 10 answers
    answers = answers.order_by("-answered_at")[:10]

    print(answers)

    ctx['display'] = {
        'username': request.user.username,
        'answers': answers,
    }

    return render(request, 'app/account.html', ctx)
