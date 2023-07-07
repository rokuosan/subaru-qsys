from app.models.category import CtfQuestionCategory
from app.models.difficulty import CtfQuestionDifficulty
from app.models.history import CtfAnswerHistory
from app.models.question import CtfQuestion
from app.models.score import CtfScore
from app.models.ctf_information import CtfInformation
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

    ctf = None
    ctfs = CtfInformation.objects.filter(is_active=True)
    if not ctfs:
        ctx["message"] = "CTFが開催されていません"
        render(request, "app/questions.html", ctx)
    for c in ctfs:
        if request.user in c.participants.all():
            ctf = c
            break

    if ctf is None:
        ctx["message"] = "CTFに参加していません"
        render(request, "app/questions.html", ctx)

    # Questionから全データを取得して、辞書型に変換
    questions = ctf.questions.all().values()
    categories = CtfQuestionCategory.objects.all().values()
    diffs = CtfQuestionDifficulty.objects.all().values()
    history = CtfAnswerHistory.objects.filter(
        user=request.user, is_correct=True
    )

    # 回答済みの問題番号を取得
    answered_ids = history.values_list("question_id", flat=True)
    # ユーザがチームに所属している場合、チームの回答済み問題番号を取得
    if request.user.team:
        team_history = CtfAnswerHistory.objects.filter(
            team=request.user.team, is_correct=True
        )
        answered_ids_by_team = team_history.values_list(
            "question_id", flat=True
        )

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

                # この問題に公開フラグが立っているか
                if not q["is_published"]:
                    continue

                # すでに回答済みか
                if q["question_id"] in answered_ids:
                    q["is_answered"] = True
                elif request.user.team:
                    if q["question_id"] in answered_ids_by_team:
                        q["is_answered"] = True
                        q["is_answered_by_team"] = True

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

        if answer.strip() == "":
            request.session["result"] = {
                "message": "回答が空です",
                "is_correct": False,
            }
            return redirect(question_detail, question_id=question_id)

        # この問題について自分が提出した回答一覧を取得
        ans_list = CtfAnswerHistory.objects.filter(
            question=question, user=request.user
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
                question=question, team=request.user.team
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
            )
            history.save()

            # スコアを保存
            score = CtfScore(
                user=request.user,
                team=request.user.team,
                question=question,
                point=question.point,
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
