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

    if ctf is None:
        default_ctf = ctfs.filter(is_active=True).first()
    else:
        default_ctf = ctf

    ctx["ctfs"] = ctfs
    ctx["selected_ctf_id"] = default_ctf.ctf_id

    histories = CtfAnswerHistory.objects.filter(ctf=default_ctf).order_by(
        "-answered_at"
    )

    history = []
    for h in histories:
        history.append(
            {
                "player": h.user.username,
                "ctf": h.ctf.name,
                "question": h.question.title,
                "content": h.content,
                "is_correct": h.is_correct,
                "answered_at": h.answered_at,
            }
        )

    ctx["history"] = history

    return render(request, "app/answer-history.html", ctx)
