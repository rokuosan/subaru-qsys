from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.models.ctf_information import CtfInformation
from app.models.history import CtfAnswerHistory


@login_required
def answer_history(request: HttpRequest):
    if not request.user.is_admin:
        messages.warning(request, "管理者権限がありません")
        return redirect("index")

    ctx = {}

    ctf = None
    default_ctf = None
    ctfs = CtfInformation.objects.all()

    param_ctf_id = request.GET.get("ctf_id")
    if param_ctf_id:
        try:
            ctf = ctfs.get(ctf_id=param_ctf_id)
        except CtfInformation.DoesNotExist:
            messages.warning(request, "CTFがありません")
            ctx["ctfs"] = ctfs.order_by("-pk")
            return render(request, "app/answer-history.html", ctx)
    else:
        if not ctfs:
            messages.warning(request, "CTFがありません")
            return render(request, "app/answer-history.html")
        for c in ctfs.filter(is_active=True):
            if request.user in c.participants.all():
                ctf = c
                break

    ctfs = ctfs.order_by("-pk")

    if ctfs is None:
        messages.warning(request, "CTFがありません")
        return render(request, "app/answer-history.html", ctx)

    if ctf is None:
        default_ctf = ctfs.filter(is_active=True).first()
        if default_ctf is None:
            default_ctf = ctfs.first()
    else:
        default_ctf = ctf

    ctx["ctfs"] = ctfs
    ctx["selected_ctf_id"] = default_ctf.ctf_id

    selected_player = None
    param_user_id = request.GET.get("user_id")
    if param_user_id and param_user_id != "0":
        try:
            selected_player = default_ctf.participants.get(pk=param_user_id)
        except CtfAnswerHistory.DoesNotExist:
            messages.warning(request, "ユーザーが存在しません")
            return render(request, "app/answer-history.html", ctx)

    ctx["selected_player_id"] = selected_player.id if selected_player else None
    players = []
    players.append({"username": "All", "user_id": 0})
    for p in default_ctf.participants.all():
        players.append(
            {
                "username": p.username,
                "user_id": p.id,
            }
        )

    ctx["players"] = players

    if selected_player:
        histories = CtfAnswerHistory.objects.filter(
            ctf=default_ctf, user=selected_player
        ).order_by("-answered_at")
    else:
        histories = CtfAnswerHistory.objects.filter(ctf=default_ctf).order_by(
            "-answered_at"
        )

    history = []
    for h in histories:
        history.append(
            {
                "player": h.user.username,
                "ctf": h.ctf.name,
                "team": h.team if h.team else None,
                "question": h.question.title,
                "content": h.content,
                "is_correct": h.is_correct,
                "answered_at": h.answered_at,
            }
        )

    ctx["history"] = history

    return render(request, "app/answer-history.html", ctx)
