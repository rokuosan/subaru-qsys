import re
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from ctf.models.contest import Contest
from ctf.models.question import Category, Question
from ctf.models.history import History
from ctf.utils.contest_util import ContestUtils


@login_required
def questions_view(request: HttpRequest, contest_id: str):
    """開催しているCTFで公開中の問題を表示するView"""
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    cu = ContestUtils(contest)

    # 公開設定
    fun = cu.get_page_protection(request)
    if fun is not None:
        return fun[0](*fun[1], **fun[2])

    # コンテキストの初期化
    ctx = cu.set_initial_context(request)
    if ctx["player"] is None:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")

    player = ctx["player"]
    if cu.get_team_by_player(player) is None:
        messages.info(request, "チームに所属していません")
        return redirect("ctf:home", contest_id)

    sets = []
    cats = Category.objects.all()
    solved = cu.get_solved_questions(player)
    team = ctx["team"]
    solved_team = cu.get_solved_questions(team)
    for c in cats:
        qs = contest.questions.filter(category=c, is_open=True)
        if qs:
            for q in qs:
                if q in solved:
                    q.solved = True
                    q.solved_msg = "Solved"
                    q.solved_budge = "success"
                else:
                    q.solved = False
                    if q in solved_team:
                        q.solved = True
                        q.solved_msg = "Solved by team"
                        q.solved_budge = "secondary"
            sets.append({"category": c, "questions": qs})

    ctx["sets"] = sets
    ctx["total"] = sum([len(s["questions"]) for s in sets])
    ctx["solved"] = len(solved)

    return render(request, "ctf/contest/questions.html", ctx)


@login_required
def question_detail_view(
    request: HttpRequest, contest_id: str, question_id: str
):
    """開催しているCTFで公開中の問題を表示するView"""
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    question: Question = get_object_or_404(
        contest.questions.all(), id=question_id
    )
    ctx = {"contest": contest, "question": question}
    cu = ContestUtils(contest)
    try:
        player = request.user.player
    except Exception:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")
    solved = cu.get_solved_questions(player)
    solved_team = cu.get_solved_questions(cu.get_team_by_player(player))
    if question in solved:
        ctx["solved"] = True
        ctx["solved_msg"] = "Solved"
        ctx["solved_budge"] = "success"
    elif question in solved_team:
        ctx["solved"] = True
        ctx["solved_msg"] = "Solved by team"
        ctx["solved_budge"] = "secondary"

    if cu.get_team_by_player(player) is None:
        messages.info(request, "チームに所属していません")
        return redirect("ctf:home", contest_id)

    # Checks
    if not contest.is_open:
        messages.info(request, "このコンテストは非公開です")
        if not request.user.is_admin:
            return redirect("ctf:index")
    if not question.is_open:
        messages.info(request, "この問題は非公開です")
        if not request.user.is_admin:
            return redirect("ctf:index")

    if contest.status != Contest.Status.RUNNING:
        messages.info(request, "このコンテストは開催中ではありません")
        if not request.user.is_admin:
            return redirect("ctf:index")

    if request.method == "GET":
        # セッションから結果を取得
        ctx["result"] = request.session.get("result")
        request.session["result"] = None

        if question.file_path != "":
            file_name = question.file_path.split("/")[-1]
            ctx["file_name"] = file_name

        return render(request, "ctf/contest/question_detail.html", ctx)

    if request.method == "POST":
        answer = request.POST.get("answer")
        answer = re.sub(r"\s", "", answer)
        if not answer or answer == "":
            messages.warning(request, "回答が空です。判定を行いません。")
            return redirect("ctf:question_detail", contest_id, question_id)

        # 結果に表示する関数
        def set_result(alert_type, message):
            request.session["result"] = {
                "alert_type": alert_type,
                "message": message,
            }

        # 回答済み
        if question in solved:
            set_result("warning", "既に回答済みです。")
            return redirect("ctf:question_detail", contest_id, question_id)

        team = contest.get_team_by_player(player)

        question_pts = 0
        result_type = History.ResultType.INCORRECT
        if question.flag == answer:
            hist = History.objects.filter(
                contest=contest, question=question, team=team, is_correct=True
            )
            if hist.count() == 0:
                question_pts = question.point
                set_result("success", "正解！")
                result_type = History.ResultType.CORRECT
            else:
                result_type = History.ResultType.ANSWERED_BY_TEAM
                set_result("success", "正解！チームが解答済みのため点数は加算されません。")
        else:
            set_result("warning", "不正解...")

        History.objects.create(
            contest=contest,
            team=team,
            player=player,
            question=question,
            point=question_pts,
            is_correct=question.flag == answer,
            answer=answer,
            result=result_type[0],
        )

        return redirect("ctf:question_detail", contest_id, question_id)
    return render(request, "ctf/contest/questions.html", ctx)
