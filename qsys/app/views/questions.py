from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render

from ctf.models.contest import Contest
from ctf.models.player import Player
from ctf.models.history import History
from ctf.models.question import Category, Question


@login_required
def questions(request: HttpRequest):
    """問題一覧を表示するView"""
    ctx = {}

    contest = None
    player = Player.get_player(request.user)
    contests = Contest.get_active_contests()
    if not contests:
        ctx["message"] = "コンテストが開催されていません"
        return render(request, "app/questions.html", ctx)
    for c in contests:
        if player in c.get_joined_players():
            contest = c
            break

    if contest is None:
        messages.error(request, "参加中のコンテストはありません")
        return redirect("index")

    if contest.is_over:
        if request.user.is_admin:
            messages.error(request, "このコンテストの開催期間は終了しました")
            messages.info(request, "管理者として閲覧しています")
        else:
            messages.error(request, "開催期間が過ぎているため、問題を閲覧できません")
            return redirect("index")

    if contest.status == Contest.Status.PAUSED:
        if request.user.is_admin:
            messages.error(request, "CTFは一時中止されています")
            messages.info(request, "管理者として閲覧しています")
        else:
            messages.error(request, "CTFは一時中止されています")
            return redirect("index")

    # 公開中の問題を取得
    all_questions = contest.questions.filter(is_open=True)

    # 回答済みの問題を取得
    solved = History.objects.filter(
        player=player, is_correct=True, contest=contest
    ).values_list("question", flat=True)

    teams = player.teams.all()
    team = None
    for t in teams:
        if t in contest.teams.all():
            team = t
            break

    solved_team = (
        History.objects.filter(team=team, is_correct=True, contest=contest)
        .exclude(player=player)
        .values_list("question", flat=True)
    )

    # カテゴリごとに問題を分類し、リストに追加
    lst = []
    categories = Category.objects.all()
    for cat in categories:
        questions = []
        cat_questions = all_questions.filter(category=cat)
        cat_questions = cat_questions.order_by("difficulty")
        for question in cat_questions:
            if question.id in solved:
                question.is_answered = True
            elif team and question.id in solved_team:
                question.is_answered = True
                question.is_answered_by_team = True
            questions.append(question)
        lst.append({"category": cat.name, "questions": questions})

    # Capitalize category name
    for item in lst:
        item["category"] = item["category"].replace("_", " ").capitalize()

    ctx["list"] = lst

    return render(request, "app/questions.html", ctx)


@login_required
def question_detail(request: HttpRequest, question_id: str):
    """問題の詳細を表示するView"""
    ctx = {}
    question = get_object_or_404(Question, pk=question_id)
    ctx["question"] = question

    # 未公開
    if not question.is_open:
        messages.error(request, "この問題は公開されていません")
        return redirect("questions")

    # コンテストが開催されていない
    contests = Contest.get_active_contests()
    if not contests:
        messages.warning(request, "コンテストが開催されていません")
        return redirect("questions")

    # コンテストを取得
    player = Player.get_player(request.user)
    for c in contests:
        if player in c.get_joined_players():
            contest = c
            break

    # コンテストが終了済み
    if contest.is_over:
        messages.warning(request, "このコンテストは終了しました")
        if not request.user.is_admin:
            return redirect("questions")

    # コンテストが一時停止
    if contest.status == Contest.Status.PAUSED:
        messages.warning(request, "このコンテストは一時停止されています")
        if not request.user.is_admin:
            return redirect("questions")

    # 未開始
    if contest.status == Contest.Status.PREPARING:
        messages.warning(request, "このコンテストは開始されていません")
        if not request.user.is_admin:
            return redirect("questions")

    if request.method == "GET":
        # セッションからのメッセージがあれば表示
        if request.session.get("message"):
            ctx["msg"] = request.session["message"]
            del request.session["message"]

    elif request.method == "POST":
        answer = request.POST.get("answer")

        # answerを整形
        answer = answer.strip()
        answer = answer.replace(" ", "")

        # 空文字列
        if not answer:
            return redirect("question_detail", question_id=question_id)

        # 回答済み
        if History.objects.filter(
            question=question, player=player, is_correct=True
        ).exists():
            messages.error(request, "既に回答済みです")
            return redirect("question_detail", question_id=question_id)

        # 回答済み（チーム）
        team = None
        for t in player.teams.all():
            if t in contest.teams.all():
                team = t
                break

        if History.objects.filter(
            question=question, team=team, is_correct=True
        ).exists():
            messages.error(request, "既にチームで回答済みです")
            return redirect("question_detail", question_id=question_id)

        # 不正解
        if answer != question.flag:
            request.session["message"] = {
                "type": "danger",
                "text": "不正解...",
            }
        # 正解
        else:
            request.session["message"] = {
                "type": "success",
                "text": "正解!",
            }

        # 回答履歴を保存
        History.objects.create(
            contest=contest,
            question=question,
            player=player,
            team=team,
            is_correct=answer == question.flag,
            answer=answer,
            point=question.point,
        ).save()

        return redirect("question_detail", question_id=question_id)

    return render(request, "app/question_detail.html", ctx)
