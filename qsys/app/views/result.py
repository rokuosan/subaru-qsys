from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from ctf.models.contest import Contest
from ctf.models.history import History


def ranked_dict_list(scores):
    rank = 0
    prev_score = -1
    for i, score in enumerate(scores):
        if score[1] != prev_score:
            rank += 1
        scores[i] = (rank, score[0], score[1])
        prev_score = score[1]

    return [{"rank": t[0], "name": t[1], "score": t[2]} for t in scores]


@login_required
def result(request: HttpRequest):
    """The CTF Result Page"""
    if not request.user.is_admin:
        messages.error(request, "管理者権限がありません")
        return redirect("index")

    ctx = {}

    # コンテストを取得
    contests = Contest.objects.all()
    contest_id = request.GET.get("contest_id")
    if contests.count() == 0:
        messages.error(request, "コンテストが存在しません")
        return render(request, "app/result.html", ctx)
    if contest_id:
        contest = get_object_or_404(contests, pk=contest_id)
    else:
        contest = Contest.get_active_contests().first()
        if contest is None:
            contest = contests.first()

    ctx["contests"] = contests
    ctx["selected_contest_id"] = contest.id

    # CTF参加者のチームを取得
    players = contest.get_joined_players()
    teams = contest.teams.all()

    # チームごとのスコアと、ランキングを算出(ORDER BY score DESC, name ASC)
    team_scores = [(t, History.get_team_point(contest, t)) for t in teams]
    team_scores = sorted(team_scores, key=lambda x: (-x[1], x[0].name))
    team_scores = ranked_dict_list(team_scores)
    ctx["team_score_rank"] = team_scores

    # ユーザごとのスコアと、ランキングを算出(ORDER BY score DESC, name ASC)
    user_scores = [(u, History.get_player_point(contest, u)) for u in players]
    user_scores = sorted(user_scores, key=lambda x: (-x[1], x[0].name))
    user_scores = ranked_dict_list(user_scores)
    ctx["player_score_rank"] = user_scores

    # チームごとの正解率と、ランキングを算出(ORDER BY rate DESC, name ASC)
    team_rates = [(t, History.get_team_accuracy(contest, t)) for t in teams]
    team_rates = sorted(team_rates, key=lambda x: (-x[1], x[0].name))
    team_rates = ranked_dict_list(team_rates)
    for t in team_rates:
        # 正答率は小数点第2位まで表示し、％表示を行う
        t["score"] = f"{t['score']:.2%}"
        # 解答数と、正解数を表示する
        t["answered"] = History.objects.filter(
            team=t["name"], contest=contest
        ).count()
        t["correct"] = History.objects.filter(
            team=t["name"], contest=contest, is_correct=True
        ).count()
    ctx["team_rate_rank"] = team_rates

    # ユーザごとの正解率と、ランキングを算出(ORDER BY rate DESC, name ASC)
    user_rates = [
        (p, History.get_player_accuracy(contest, p)) for p in players
    ]
    user_rates = sorted(user_rates, key=lambda x: (-x[1], x[0].name))
    user_rates = ranked_dict_list(user_rates)
    for p in user_rates:
        # 正答率は小数点第2位まで表示し、％表示を行う
        p["score"] = f"{p['score']:.2%}"
        # 解答数と、正解数を表示する
        p["answered"] = History.objects.filter(
            player=p["name"], contest=contest
        ).count()
        p["correct"] = History.objects.filter(
            player=p["name"], contest=contest, is_correct=True
        ).count()
    ctx["player_rate_rank"] = user_rates

    # よく解かれた問題を取得
    freq = History.get_frequently_solved(contest)
    for i, f in enumerate(freq):
        f["rank"] = i + 1
    ctx["frequently_solved"] = freq

    return render(request, "app/result.html", ctx)
