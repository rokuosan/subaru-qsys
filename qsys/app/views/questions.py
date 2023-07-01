import datetime

from app.models.category import CtfQuestionCategory
from app.models.ctf_information import CtfInformation
from app.models.difficulty import CtfQuestionDifficulty
from app.models.history import CtfAnswerHistory
from app.models.question import CtfQuestion
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render


@login_required
def questions(request: HttpRequest):
    """問題一覧を表示するView"""
    ctx = {
        # 'list': [{
        #     'category': 'category_name',
        #     'questions': [],
        # }]
        "list": []
    }

    # Questionから全データを取得して、辞書型に変換
    questions = CtfQuestion.objects.all().values()
    categories = CtfQuestionCategory.objects.all().values()
    diffs = CtfQuestionDifficulty.objects.all().values()

    # カテゴリ名を持った辞書を作成し、ctx['list']に追加
    for c in categories:
        info = {}
        info["category"] = c["name"]
        ctx["list"].append(info)

    # 問題データに難易度名を追加し、カテゴリが対応するctx['list']に追加
    for q in questions:
        cn = categories.get(pk=q["category_id"])["name"]
        dn = diffs.get(difficulty_id=q["difficulty_id"])["name"]

        for li in ctx["list"]:
            if li["category"] == cn:
                if "questions" not in li.keys():
                    li["questions"] = []

                q["difficulty_name"] = dn
                li["questions"].append(q)
                break

    # カテゴリ名をcapitalize
    for li in ctx["list"]:
        li["category"] = li["category"].replace("_", " ").capitalize()

    return render(request, "app/questions.html", ctx)


def question_detail(request: HttpRequest, question_id: int):
    """問題の詳細を表示するView"""
    ctx = {}
    question = get_object_or_404(CtfQuestion, pk=question_id)
    ctx["question"] = question

    if request.method == "POST":
        answer = request.POST.get("answer")

        list = CtfAnswerHistory.objects.filter(
            question=question, user=request.user, is_correct=True
        )

        if list.exists():
            request.session["result"] = {
                "message": "回答済みです",
                "is_correct": False,
            }
            return redirect(question_detail, question_id=question_id)

        if answer == question.flag:
            # 正解履歴を保存
            history = CtfAnswerHistory(
                question=question,
                user=request.user,
                content=answer,
                is_correct=True,
            )
            history.save()

            request.session["result"] = {
                "message": "正解！",
                "is_correct": True,
            }
        else:
            history = CtfAnswerHistory(
                question=question,
                user=request.user,
                content=answer,
                is_correct=False,
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
