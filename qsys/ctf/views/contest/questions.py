from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from ctf.models.contest import Contest
from ctf.models.question import Category, Question
from ctf.models.history import History


@login_required
def questions_view(request: HttpRequest, contest_id: str):
    """開催しているCTFで公開中の問題を表示するView"""
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    ctx = {"contest": contest}
    if not contest.is_open:
        messages.info(request, "このコンテストは非公開です")
        if not request.user.is_admin:
            return redirect("ctf:index")

    if contest.status != Contest.Status.RUNNING:
        messages.info(request, "このコンテストは開催中ではありません")
        if not request.user.is_admin:
            return redirect("ctf:index")

    try:
        player = request.user.player
    except Exception:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")

    sets = []
    cats = Category.objects.all()
    for c in cats:
        qs = c.questions.filter(is_open=True).order_by("point")
        if qs:
            solved = History.get_player_solved(contest, player)
            for q in qs:
                if q.id in solved.values_list("question", flat=True):
                    q.solved = True
                else:
                    q.solved = False
            sets.append({"category": c, "questions": qs})

    print(sets)
    print(solved)
    ctx["sets"] = sets
    ctx["total"] = sum([len(s["questions"]) for s in sets])
    ctx["solved"] = History.get_player_solved_count(contest, player)

    return render(request, "ctf/contest/questions.html", ctx)


@login_required
def question_detail_view(
    request: HttpRequest, contest_id: str, question_id: int
):
    """開催しているCTFで公開中の問題を表示するView"""
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    question: Question = get_object_or_404(Question, id=question_id)
    ctx = {"contest": contest, "question": question}

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
        return render(request, "ctf/contest/question_detail.html", ctx)

    return render(request, "ctf/contest/questions.html", ctx)
