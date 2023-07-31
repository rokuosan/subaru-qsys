from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from app.models.ctf_information import CtfInformation
from app.models.history import CtfAnswerHistory as history
from app.forms.score_setting import ScoreSettingForm


@login_required
def ranking(request: HttpRequest):
    user = request.user

    ctx = {}
    ctfs = CtfInformation.objects.filter(is_active=True)

    # CTFを取得
    if ctfs.count() == 0:
        messages.error(request, "CTFが作成されていません")
        return render(request, "app/ranking.html", ctx)
    ctf = ctfs.first()

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
    teams = ctf.get_teams(ctf_id=ctf.ctf_id)

    # チームごとのスコアを算出
    team_scores = [
        {"name": t.name, "score": history.get_team_point(t, ctf)}
        for t in teams
    ]

    # スコアで降順にソート
    team_scores = sorted(team_scores, key=lambda x: (-x["score"], x["name"]))

    # チームのスコアをもとにランキングを算出し、同値の場合は次の順位を飛ばす
    rank = 0
    prev_score = -1
    for i, score in enumerate(team_scores):
        if score["score"] != prev_score:
            rank += 1
        score["rank"] = rank
        prev_score = score["score"]

    # ユーザーごとのスコアを算出
    player_scores = [
        {"name": u.username, "score": history.get_user_point(u, ctf)}
        for u in users
    ]
    # ソート
    player_scores = sorted(
        player_scores, key=lambda x: (-x["score"], x["name"])
    )
    # ランキング処理
    rank = 0
    prev_score = -1
    for i, score in enumerate(player_scores):
        if score["score"] != prev_score:
            rank += 1
        score["rank"] = rank
        prev_score = score["score"]

    # ランキングを表示
    user = request.user
    if ctf.show_team_ranking or user.is_admin:
        ctx["team_score_rank"] = team_scores
        if not ctf.show_team_ranking:
            messages.info(request, "チームランキングは現在非公開です。管理者のみ表示されます。")
    if ctf.show_player_ranking or user.is_admin:
        ctx["player_score_rank"] = player_scores
        if not ctf.show_player_ranking:
            messages.info(request, "プレイヤーランキングは現在非公開です。管理者のみ表示されます。")

    ctx["is_active"] = True
    return render(request, "app/ranking.html", ctx)
