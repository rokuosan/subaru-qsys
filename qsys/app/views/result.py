from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from app.models.ctf_information import CtfInformation
from app.models.score import CtfScore


@login_required
def result(request: HttpRequest):
    """The CTF Result Page"""
    if not request.user.is_admin:
        messages.error(request, "管理者権限がありません")
        return redirect("index")

    ctx = {}

    # CTFを取得
    ctfs = CtfInformation.objects.all()
    ctf_id = request.GET.get("ctf_id")
    if ctf_id:
        try:
            ctf = ctfs.get(ctf_id=ctf_id)
        except CtfInformation.DoesNotExist:
            messages.error(request, "そのようなCTFは存在しません")
            return render(request, "app/result.html", ctx)
    else:
        ctf = ctfs.filter(is_active=True).first()
        if ctf is None:
            ctf = ctfs.first()

    ctx["ctfs"] = ctfs
    ctx["selected_ctf_id"] = ctf.ctf_id

    # CTF参加者のチームを取得
    users = ctf.participants.all()
    teams = []
    for user in users:
        if not user.team:
            continue
        if user.team not in teams:
            teams.append(user.team)

    # チームごとのスコアを算出
    all_scores = CtfScore.objects.all()
    team_scores = []
    for team in teams:
        team_score = 0
        for score in all_scores:
            if score.user.team == team:
                team_score += score.point
        team_scores.append((team, team_score))

    # ORDER BY score DESC, team_name ASC
    team_scores = sorted(team_scores, key=lambda x: (-x[1], x[0].name))

    # チームごとの順位を付与(同順位が続く場合は、次の順位を飛ばす)
    rank = 1
    prev_score = -1
    for i, team_score in enumerate(team_scores):
        if team_score[1] != prev_score:
            rank = i + 1
        team_scores[i] = (rank, team_score[0], team_score[1])
        prev_score = team_score[1]

    # 辞書型に変換
    team_scores = [{
        "rank": t[0],
        "name": t[1],
        "score": t[2]} for t in team_scores]

    ctx["team_score_rank"] = team_scores

    # ユーザごとのスコアを算出
    user_scores = []
    for user in users:
        user_score = 0
        for score in all_scores:
            if score.user == user:
                user_score += score.point
        user_scores.append((user, user_score))

    # ORDER BY score DESC, user_name ASC
    user_scores = sorted(user_scores, key=lambda x: (-x[1], x[0].username))

    # ユーザごとの順位を付与(同順位が続く場合は、次の順位を飛ばす)
    rank = 1
    prev_score = -1
    for i, user_score in enumerate(user_scores):
        if user_score[1] != prev_score:
            rank = i + 1
        user_scores[i] = (rank, user_score[0], user_score[1])
        prev_score = user_score[1]

    # 辞書型に変換
    user_scores = [{
        "rank": t[0],
        "name": t[1],
        "score": t[2]} for t in user_scores]

    ctx["player_score_rank"] = user_scores

    return render(request, "app/result.html", ctx)
