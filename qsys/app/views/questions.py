from app.models.category import CtfQuestionCategory
from app.models.history import CtfAnswerHistory as history
from app.models.question import CtfQuestion
from app.models.ctf_information import CtfInformation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render


@login_required
def questions(request: HttpRequest):
    """問題一覧を表示するView"""
    ctx = {}

    ctf = None
    ctfs = CtfInformation.objects.filter(is_active=True)
    if not ctfs:
        ctx["message"] = "CTFが開催されていません"
        return render(request, "app/questions.html", ctx)
    for c in ctfs:
        if request.user in c.participants.all():
            ctf = c
            break

    if ctf is None:
        messages.error(request, "参加中のCTFはありません")
        return redirect("index")

    if ctf.is_ended:
        if request.user.is_admin:
            messages.error(request, "このCTFの開催期間は終了しました")
            messages.info(request, "管理者として閲覧しています")
        else:
            messages.error(request, "開催期間が過ぎているため、問題を閲覧できません")
            return redirect("index")

    if ctf.is_paused:
        if request.user.is_admin:
            messages.error(request, "CTFは一時中止されています")
            messages.info(request, "管理者として閲覧しています")
        else:
            messages.error(request, "CTFは一時中止されています")
            return redirect("index")

    # 公開中の問題を取得
    all_questions = CtfQuestion.objects.filter(is_published=True)

    # 回答済みの問題を取得
    solved = history.objects.filter(
        user=request.user, is_correct=True, ctf=ctf
    ).values_list("question", flat=True)
    print(solved)
    solved_team = None
    if request.user.team:
        solved_team = (
            history.objects.filter(
                team=request.user.team, is_correct=True
            ).exclude(user=request.user)
        ).values_list("question", flat=True)

    # カテゴリごとに問題を分類し、リストに追加
    lst = []
    categories = CtfQuestionCategory.objects.all()
    for cat in categories:
        questions = []
        cat_questions = all_questions.filter(category=cat)
        cat_questions = cat_questions.order_by("difficulty")
        for question in cat_questions:
            if question.question_id in solved:
                question.is_answered = True
            elif request.user.team and question.question_id in solved_team:
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
def question_detail(request: HttpRequest, question_id: int):
    """問題の詳細を表示するView"""
    ctx = {}
    question = get_object_or_404(CtfQuestion, pk=question_id)
    ctx["question"] = question

    # 未公開
    if not question.is_published:
        messages.error(request, "この問題は公開されていません")
        return redirect("questions")

    # CTFが開催されていない
    ctfs = CtfInformation.objects.filter(is_active=True)
    if not ctfs:
        messages.warning(request, "CTFが開催されていません")
        return redirect("questions")

    # CTFが終了済み
    ctf = ctfs.first()
    if ctf.is_ended:
        messages.warning(request, "このCTFは終了しました")
        if not request.user.is_admin:
            return redirect("questions")

    # CTFが一時停止
    if ctf.is_paused:
        messages.warning(request, "このCTFは一時停止されています")
        if not request.user.is_admin:
            return redirect("questions")

    # 未開始
    if not ctf.is_started:
        messages.warning(request, "このCTFは開始されていません")
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
        if history.objects.filter(
            question=question, user=request.user, is_correct=True
        ).exists():
            messages.error(request, "既に回答済みです")
            return redirect("question_detail", question_id=question_id)

        # 回答済み（チーム）
        if (
            request.user.team
            and history.objects.filter(
                question=question, team=request.user.team, is_correct=True
            ).exists()
        ):
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
        history.objects.create(
            question=question,
            user=request.user,
            team=request.user.team,
            is_correct=answer == question.flag,
            content=answer,
            ctf=ctf,
        ).save()

        return redirect("question_detail", question_id=question_id)

    return render(request, "app/question_detail.html", ctx)
