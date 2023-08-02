from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from ctf.models.history import History
from ctf.models.contest import Contest
from ctf.models.player import Player


@login_required
def ranking(request: HttpRequest):

    ctx = {}

    contests = Contest.get_active_contests()
    if not contests:
        messages.warning(request, "コンテストが開催されていません")
        return render(request, "app/ranking.html", ctx)
    contest = None
    player = Player.get_player(request.user)
    for c in contests:
        if player in c.get_joined_players():
            contest = c
            break

    if contest is None:
        messages.warning(request, "コンテストに参加していません")
        return render(request, "app/ranking.html", ctx)

    if request.user.is_admin:
        # ctx["form"] = ScoreSettingForm(ctf=ctf)
        pass

    # if request.method == "POST":
    #     show_team = request.POST.get("show_team_rankinng")
    #     show_player = request.POST.get("show_player_ranking")

    #     ctf.show_team_ranking = show_team == "on"
    #     ctf.show_player_ranking = show_player == "on"

    #     ctf.save()

    #     return redirect("ranking")

    # CTF参加者のチームを取得
    players = contest.get_joined_players()
    teams = contest.teams.all()

    # チームごとのスコアを算出
    team_scores = [
        {"name": t.name, "score": History.get_team_point(contest, t)}
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
        {"name": u.name, "score": History.get_player_point(contest, u)}
        for u in players
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
    if contest.is_team_ranking_public or request.user.is_admin:
        ctx["team_score_rank"] = team_scores
        if not contest.is_team_ranking_public:
            messages.info(request, "チームランキングは現在非公開です。管理者のみ表示されます。")
    if contest.is_player_ranking_public or request.user.is_admin:
        ctx["player_score_rank"] = player_scores
        if not contest.is_player_ranking_public:
            messages.info(request, "プレイヤーランキングは現在非公開です。管理者のみ表示されます。")

    ctx["is_active"] = True
    return render(request, "app/ranking.html", ctx)
