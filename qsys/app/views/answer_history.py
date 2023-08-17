from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ctf.models.contest import Contest
from ctf.models.player import Player
from ctf.models.history import History


@login_required
def answer_history(request: HttpRequest):
    if not request.user.is_admin:
        messages.warning(request, "管理者権限がありません")
        return redirect("index")

    ctx = {}

    contest = None
    default_contest = None
    contests = Contest.objects.all()
    player = Player.get_player(request.user)

    param_contest_id = request.GET.get("contest_id")
    if param_contest_id:
        contest = get_object_or_404(contests, pk=param_contest_id)
    else:
        if not contests:
            messages.warning(request, "コンテストが登録されていません")
            return render(request, "app/answer-history.html")
        for c in Contest.get_active_contests():
            if player in c.get_joined_players():
                contest = c
                break

    contests = contests.order_by("-pk")

    if contests is None:
        messages.warning(request, "コンテストがありません")
        return render(request, "app/answer-history.html", ctx)

    if contest is None:
        default_contest = Contest.get_active_contests().first()
        if default_contest is None:
            default_contest = contests.first()
    else:
        default_contest = contest

    print(contests)
    ctx["contests"] = contests
    ctx["selected_contest_id"] = (
        default_contest.id if default_contest else None
    )

    selected_player = None
    param_player_id = request.GET.get("player_id")
    if param_player_id and param_player_id != "0":
        selected_player = get_object_or_404(
            Player, pk=param_player_id, user__is_active=True
        )

    ctx["selected_player_id"] = selected_player.id if selected_player else None
    players = []
    players.append({"username": "All", "player_id": 0})
    for p in Contest.get_joined_players(default_contest):
        players.append(
            {
                "username": p.name,
                "player_id": p.id,
            }
        )

    ctx["players"] = players

    if selected_player:
        histories = History.objects.filter(
            contest=default_contest, player=selected_player
        ).order_by("-created_at")
    else:
        histories = History.objects.filter(contest=default_contest).order_by(
            "-created_at"
        )

    history = []
    for h in histories:
        history.append(
            {
                "player": h.player.name,
                "contest": h.contest.name,
                "team": h.team if h.team else None,
                "question": h.question.title,
                "content": h.answer,
                "is_correct": h.is_correct,
                "answered_at": h.created_at,
            }
        )

    ctx["history"] = history

    return render(request, "app/answer-history.html", ctx)
