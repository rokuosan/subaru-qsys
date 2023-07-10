from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from app.models.ctf_information import CtfInformation
from app.models.score import CtfScore
from .index import index


@login_required
def score(request: HttpRequest):
    user = request.user
    if not user.is_admin:
        return redirect(index)

    ctx = {}
    ctfs = CtfInformation.objects.all()
    scores = CtfScore.objects.all()

    # CTFを取得
    if not ctfs.filter(is_active=True):
        messages.warning(request, "開催中のCTFがありません")
        return render(request, "app/score.html", ctx)
    for c in ctfs:
        if request.user in c.participants.all():
            ctf = c
            break

    if ctf is None:
        messages.warning(request, "CTFに参加していません")
        return render(request, "app/score.html", ctx)

    # CTF参加者のチームを取得
    users = ctf.participants.all()
    teams = []
    for user in users:
        if not user.team:
            continue
        if user.team not in teams:
            teams.append(user.team)

    # チームごとのスコアを算出
    team_scores = []
    for team in teams:
        team_score = 0
        for score in scores:
            if score.user.team == team:
                team_score += score.point
        team_scores.append(team_score)

    # チームごとのスコアを降順にソート
    team_score_set = []
    for team in teams:
        idx = teams.index(team)
        team_score_set.append(
            {
                "name": team.name,
                "score": team_scores[idx],
                "rank": idx + 1,
            }
        )
    team_score_set = sorted(
        team_score_set, key=lambda x: x["score"], reverse=True
    )

    # ユーザーごとのスコアを算出
    player_scores = []
    for user in users:
        user_score = 0
        for score in scores:
            if score.user == user:
                user_score += score.point
        player_scores.append(user_score)

    # ユーザーごとのスコアを降順にソート
    player_score_set = []
    for i, u in enumerate(users):
        player_score_set.append(
            {
                "name": u.username,
                "score": player_scores[i],
                "rank": i + 1,
            }
        )
    player_score_set = sorted(
        player_score_set, key=lambda x: x["score"], reverse=True
    )

    # ランキングを表示
    ctx["player_score_rank"] = player_score_set
    ctx["team_score_rank"] = team_score_set

    return render(request, "app/score.html", ctx)
