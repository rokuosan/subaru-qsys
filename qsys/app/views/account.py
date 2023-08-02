from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from ctf.models.player import Player
from ctf.models.contest import Contest
from ctf.models.history import History


@login_required
def account(request: HttpRequest):
    ctx = {}
    player = Player.get_player(request.user)
    if player is None:
        messages.warning(request, "プレイヤー情報がありません")
        return redirect("index")

    ctx["display"] = {
        "username": player.name,
        "team": "-",
        "answers": [],
        "point": 0,
        "ratio": 0,
        "team_ratio": "-",
        "team_point": "-",
    }

    contest = None
    contests = Contest.get_active_contests()
    if not contests:
        messages.warning(request, "コンテストが開催されていません")
        return render(request, "app/account.html", ctx)
    for c in contests:
        if player in c.get_joined_players():
            contest = c
            break

    if contest is None:
        messages.warning(request, "コンテストに参加していません")
        return render(request, "app/account.html", ctx)

    # Get last newest 10 Answers
    answers = History.objects.filter(player=player, contest=contest).order_by(
        "-created_at"
    )[:10]

    # Your point
    point = History.get_player_point(contest, player)

    # Answer ratio
    ac = History.get_player_accuracy(contest, player)

    team = None
    for t in contest.teams.all():
        if player in t.members.all():
            team = t
            break
    if team is None:
        messages.warning(request, "チームに所属していません")
        return render(request, "app/account.html", ctx)

    ctx["display"] = {
        "username": player.name,
        "team": team,
        "answers": answers,
        "point": point,
        "ratio": round(ac, 2),
        "team_ratio": "-",
        "team_point": "-",
    }

    tac = History.get_team_accuracy(contest, team)
    tpt = History.get_team_point(contest, team)

    ctx["display"]["team_ratio"] = round(tac, 2)
    ctx["display"]["team_point"] = tpt

    return render(request, "app/account.html", ctx)
