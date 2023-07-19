from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from app.models.ctf_information import CtfInformation
from app.models.score import CtfScore
from app.forms.score_setting import ScoreSettingForm


@login_required
def ranking(request: HttpRequest):
    user = request.user

    ctx = {}
    ctfs = CtfInformation.objects.all()
    scores = CtfScore.objects.all()

    # CTFを取得
    ctf = None
    if not ctfs.filter(is_active=True):
        messages.warning(request, "開催中のCTFがありません")
        return render(request, "app/ranking.html", ctx)
    for c in ctfs:
        if request.user in c.participants.all():
            ctf = c
            break

    if ctf is None:
        messages.warning(request, "CTFに参加していません")
        return render(request, "app/ranking.html", ctx)

    if user.is_admin:
        ctx["form"] = ScoreSettingForm(ctf=ctf)

    if request.method == "POST":
        show_team = request.POST.get("show_team_rankinng")
        show_player = request.POST.get("show_player_ranking")

        ctf.show_team_ranking = show_team == "on"
        ctf.show_player_ranking = show_player == "on"

        ctf.save()

        return redirect("ranking")

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
            }
        )
    team_score_set = sorted(
        team_score_set, key=lambda x: x["score"], reverse=True
    )
    for i, t in enumerate(team_score_set):
        t["rank"] = i + 1

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
            }
        )
    player_score_set = sorted(
        player_score_set, key=lambda x: x["score"], reverse=True
    )
    for i, p in enumerate(player_score_set):
        p["rank"] = i + 1
    player_score_set = player_score_set[:10]

    # ランキングを表示
    user = request.user
    if ctf.show_team_ranking or user.is_admin:
        ctx["team_score_rank"] = team_score_set
        if not ctf.show_team_ranking:
            messages.info(request, "チームランキングは現在非公開です。管理者のみ表示されます。")
    if ctf.show_player_ranking or user.is_admin:
        ctx["player_score_rank"] = player_score_set
        if not ctf.show_player_ranking:
            messages.info(request, "プレイヤーランキングは現在非公開です。管理者のみ表示されます。")

    ctx["is_active"] = True
    return render(request, "app/ranking.html", ctx)
