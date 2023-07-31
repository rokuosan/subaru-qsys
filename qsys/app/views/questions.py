from app.models.category import CtfQuestionCategory
from app.models.history import CtfAnswerHistory
from app.models.question import CtfQuestion
from app.models.score import CtfScore
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
        ctx["message"] = "CTFに参加していません"
        return render(request, "app/questions.html", ctx)

    if ctf.is_ended:
        messages.error(request, "開催期間が過ぎているため、問題を閲覧できません")
        return redirect("index")

    if ctf.is_paused:
        messages.error(request, "CTFは一時中止されています")
        return redirect("index")

    # 公開中の問題を取得
    all_questions = CtfQuestion.objects.filter(is_published=True)

    # 回答済みの問題を取得
    solved_ids = CtfAnswerHistory.objects.filter(
        user=request.user, is_correct=True
    ).values_list("question_id")
    solved_ids_team = None
    if request.user.team:
        solved_ids_team = CtfAnswerHistory.objects.filter(
            team=request.user.team, is_correct=True
        ).exclude(user=request.user).values_list("question_id")

    # カテゴリごとに問題を分類し、リストに追加
    lst = []
    categories = CtfQuestionCategory.objects.all()
    for cat in categories:
        questions = []
        cat_questions = all_questions.filter(category=cat)
        cat_questions = cat_questions.order_by("difficulty")
        for question in cat_questions:
            if question.question_id in solved_ids:
                question["is_answered"] = True
            elif request.user.team and question.id in solved_ids_team:
                question["is_answered"] = True
                question["is_answered_by_team"] = True
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

    if not question.is_published:
        messages.error(request, "この問題は公開されていません")
        if not request.user.is_admin:
            return redirect("questions")
        else:
            messages.info(request, "管理者のため、問題を閲覧できます")

    # Get previous url
    prev_url = request.META.get("HTTP_REFERER")
    current_url = request.build_absolute_uri()
    if prev_url is None:
        prev_url = current_url

    if prev_url != current_url:
        ctx["prev_url"] = prev_url
    else:
        pass

    if request.method == "POST":
        answer = request.POST.get("answer")

        ctf = None
        ctfs = CtfInformation.objects.filter(is_active=True)
        if not ctfs:
            request.session["result"] = {
                "message": "CTFが開催されていません",
                "is_correct": False,
            }
            return redirect(question_detail, question_id=question_id)
        for c in ctfs:
            if request.user in c.participants.all():
                ctf = c
                break

        if ctf is None:
            request.session["result"] = {
                "message": "CTFに参加していません",
                "is_correct": False,
            }
            return redirect(question_detail, question_id=question_id)

        if ctf.is_ended:
            request.session["result"] = {
                "message": "開催期間が切れています",
                "is_correct": False,
            }
            return redirect(question_detail, question_id=question_id)

        if answer.strip() == "":
            request.session["result"] = {
                "message": "回答が空です",
                "is_correct": False,
            }
            return redirect(question_detail, question_id=question_id)

        # CTFが一時中止なら回答不可
        if ctf.is_paused:
            request.session["result"] = {
                "message": "CTFは一時中止されています",
                "is_correct": False,
            }
            return redirect(question_detail, question_id=question_id)

        # この問題について自分が提出した回答一覧を取得
        ans_list = CtfAnswerHistory.objects.filter(
            question=question, user=request.user, ctf=ctf
        )

        # すでに正解を回答済みか
        if ans_list.filter(is_correct=True).exists():
            request.session["result"] = {
                "message": "正解を回答済みです",
                "is_correct": False,
            }
            return redirect(question_detail, question_id=question_id)

        # この問題についてチームが提出した回答一覧を取得
        if request.user.team:
            team_ans_list = CtfAnswerHistory.objects.filter(
                question=question, team=request.user.team, ctf=ctf
            )

            # チームがすでに正解を回答済みか
            if team_ans_list.filter(is_correct=True).exists():
                request.session["result"] = {
                    "message": "チームが回答済みです",
                    "is_correct": False,
                }
                return redirect(question_detail, question_id=question_id)

        if answer == question.flag:
            # 正解履歴を保存
            history = CtfAnswerHistory(
                question=question,
                user=request.user,
                team=request.user.team,
                content=answer,
                is_correct=True,
                ctf=ctf,
            )
            history.save()

            # スコアを保存
            score = CtfScore(
                user=request.user,
                team=request.user.team,
                question=question,
                point=question.point,
                ctf=ctf,
            )
            score.save()

            request.session["result"] = {
                "message": "正解！",
                "is_correct": True,
            }
        else:
            history = CtfAnswerHistory(
                question=question,
                user=request.user,
                team=request.user.team,
                content=answer,
                is_correct=False,
                ctf=ctf,
            )
            history.save()

            request.session["result"] = {
                "message": "不正解",
                "is_correct": False,
            }

        return redirect(question_detail, question_id=question_id)

    elif request.method == "GET":
        # セッションからcontextを取得
        if "result" in request.session.keys():
            res = request.session["result"]
            ctx["message"] = res["message"]
            ctx["is_correct"] = res["is_correct"]
            del request.session["result"]

    return render(request, "app/question_detail.html", ctx)
