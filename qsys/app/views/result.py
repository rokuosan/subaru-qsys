from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect, render

from app.models.ctf_information import CtfInformation
from app.models.history import CtfAnswerHistory as history


def ranked_dict_list(scores):
    rank = 1
    prev_score = -1
    for i, score in enumerate(scores):
        if score[1] != prev_score:
            rank = i + 1
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

    # CTFを取得
    ctfs = CtfInformation.objects.all()
    ctf_id = request.GET.get("ctf_id")
    if ctfs.count() == 0:
        messages.error(request, "CTFが存在しません")
        return render(request, "app/result.html", ctx)
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
    teams = ctf.get_teams(ctf.ctf_id)

    # チームごとのスコアと、ランキングを算出(ORDER BY score DESC, name ASC)
    team_scores = [(t, history.get_team_point(t, ctf)) for t in teams]
    team_scores = sorted(team_scores, key=lambda x: (-x[1], x[0].name))
    team_scores = ranked_dict_list(team_scores)
    ctx["team_score_rank"] = team_scores

    # ユーザごとのスコアと、ランキングを算出(ORDER BY score DESC, name ASC)
    user_scores = [(u, history.get_user_point(u, ctf)) for u in users]
    user_scores = sorted(user_scores, key=lambda x: (-x[1], x[0].username))
    user_scores = ranked_dict_list(user_scores)
    ctx["player_score_rank"] = user_scores

    # チームごとの正解率と、ランキングを算出(ORDER BY rate DESC, name ASC)
    team_rates = [(t, history.get_team_accuracy(t, ctf)) for t in teams]
    team_rates = sorted(team_rates, key=lambda x: (-x[1], x[0].name))
    team_rates = ranked_dict_list(team_rates)
    for t in team_rates:
        # 正答率は小数点第2位まで表示し、％表示を行う
        t["score"] = f"{t['score']:.2%}"
        # 解答数と、正解数を表示する
        t["answered"] = history.objects.filter(team=t["name"], ctf=ctf).count()
        t["correct"] = history.objects.filter(
            team=t["name"], ctf=ctf, is_correct=True
        ).count()
    ctx["team_rate_rank"] = team_rates

    # ユーザごとの正解率と、ランキングを算出(ORDER BY rate DESC, name ASC)
    user_rates = [(u, history.get_user_accuracy(u, ctf)) for u in users]
    user_rates = sorted(user_rates, key=lambda x: (-x[1], x[0].username))
    user_rates = ranked_dict_list(user_rates)
    for u in user_rates:
        # 正答率は小数点第2位まで表示し、％表示を行う
        u["score"] = f"{u['score']:.2%}"
        # 解答数と、正解数を表示する
        u["answered"] = history.objects.filter(user=u["name"], ctf=ctf).count()
        u["correct"] = history.objects.filter(
            user=u["name"], ctf=ctf, is_correct=True
        ).count()
    ctx["player_rate_rank"] = user_rates

    # よく解かれた問題を取得
    freq = history.get_frequently_solved(ctf, False)
    for i, f in enumerate(freq):
        f["rank"] = i + 1
    ctx["frequently_solved"] = freq

    return render(request, "app/result.html", ctx)
