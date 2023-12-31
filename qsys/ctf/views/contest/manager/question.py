import os
import re
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings

from ctf.models.contest import Contest
from ctf.models.question import Question, Category, Difficulty
from ctf.utils.contest_util import ContestUtils


@login_required
def manager_question_view(request: HttpRequest, contest_id: str):
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    cu = ContestUtils(contest)

    if not request.user.is_admin:
        return redirect("ctf:home", contest_id=contest.id)

    # 公開設定
    fun = cu.get_page_protection(request)
    if fun is not None:
        return fun[0](*fun[1], **fun[2])

    # コンテキストの初期化
    ctx = cu.set_initial_context(request)
    if ctx["player"] is None:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")
    ctx["msg"] = "このページでは、問題に関する操作を行うことができます。問題についてはドキュメントを参照してください。"

    questions = contest.questions.all().order_by(
        "category_id", "difficulty_id"
    )
    ctx["questions"] = questions
    category = Category.objects.all()
    ctx["category"] = category
    difficulty = Difficulty.objects.all()
    ctx["difficulty"] = difficulty

    return render(request, "ctf/contest/manager/question.html", ctx)


@login_required
def manager_question_create_view(request: HttpRequest, contest_id: str):
    contest = get_object_or_404(Contest, id=contest_id)
    cu = ContestUtils(contest)

    if not request.user.is_admin:
        return redirect("ctf:home", contest_id=contest.id)

    if request.method != "POST":
        return redirect("ctf:manager_question", contest_id=contest.id)

    # 公開設定
    fun = cu.get_page_protection(request)
    if fun is not None:
        return fun[0](*fun[1], **fun[2])

    # コンテキストの初期化
    ctx = cu.set_initial_context(request)
    if ctx["player"] is None:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")

    create_type = request.POST.get("create_type")

    if create_type == "question":
        # 値の取得
        title = request.POST.get("title")
        description = request.POST.get("description")
        flag = request.POST.get("flag")
        point = request.POST.get("point")
        category = request.POST.get("category")
        difficulty = request.POST.get("difficulty")
        is_open = request.POST.get("is_open") == "True"
        file = request.FILES.get("file")

        # 問題タイトルのチェック
        title = title.strip()
        title = re.sub(r"\s+", " ", title)
        if len(title) < 4 or len(title) > 128:
            messages.error(request, "問題タイトルは4文字以上128文字以下で入力してください")
            return redirect("ctf:manager_question", contest_id=contest.id)

        # フラッグのチェック
        flag = flag.strip()
        flag = re.sub(r"\s+", " ", flag)
        if len(flag) < 4 or len(flag) > 128:
            messages.error(request, "flagは4文字以上128文字以下で入力してください")
            return redirect("ctf:manager_question", contest_id=contest.id)
        if re.search(r"\s+", flag) is not None:
            messages.error(request, "flagに空白文字を入れることはできません")
            return redirect("ctf:manager_question", contest_id=contest.id)

        # ポイントのチェック
        try:
            f = float(point)
        except ValueError:
            messages.error(request, "ポイントは数値で入力してください")
            return redirect("ctf:manager_question", contest_id=contest.id)
        if not f.is_integer():
            messages.error(request, "ポイントは整数で入力してください")
            return redirect("ctf:manager_question", contest_id=contest.id)
        point = int(f)
        if point < 0:
            messages.error(request, "ポイントは0以上で入力してください")
            return redirect("ctf:manager_question", contest_id=contest.id)

        # カテゴリのチェック
        try:
            category = Category.objects.get(pk=int(category))
        except ValueError:
            messages.error(request, "カテゴリの値が不正です")
            return redirect("ctf:manager_question", contest_id=contest.id)

        # 難易度のチェック
        try:
            difficulty = Difficulty.objects.get(pk=int(difficulty))
        except ValueError:
            messages.error(request, "難易度の値が不正です")
            return redirect("ctf:manager_question", contest_id=contest.id)

        # 問題文のチェック
        if description == "":
            description = title

        # 問題の作成
        try:
            question = Question(
                title=title,
                description=description,
                flag=flag,
                point=point,
                category=category,
                difficulty=difficulty,
                is_open=is_open,
            )
            question.save()
            contest.questions.add(question)
            contest.save()
            if file is not None:
                path = os.path.join(
                    settings.BASE_DIR,
                    "static",
                    "questions",
                    str(question.id),
                    file.name,
                )
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                    question.file_path = os.path.join(
                        "static", "questions", str(question.id), file.name
                    )
                    question.save()
        except Exception as e:
            print(e)
            messages.error(request, "問題の作成に失敗しました")
            return redirect("ctf:manager_question", contest_id=contest.id)

        messages.success(request, "問題を作成しました")

        return redirect("ctf:manager_question", contest_id=contest.id)

    elif create_type == "category":
        try:
            category_name = request.POST.get("category_name")
            category_name = category_name.strip()
            if category_name == "":
                messages.error(request, "カテゴリ名を入力してください")
                return redirect("ctf:manager_question", contest_id=contest.id)
            if len(category_name) > 32:
                messages.error(request, "カテゴリ名は32文字以下で入力してください")
                return redirect("ctf:manager_question", contest_id=contest.id)
            category = Category(name=category_name)
            category.save()
            messages.success(request, "カテゴリを作成しました")
        except Exception:
            messages.error(request, "カテゴリの作成に失敗しました")
        return redirect("ctf:manager_question", contest_id=contest.id)
    elif create_type == "difficulty":
        try:
            diff_name = request.POST.get("difficulty_name")
            diff_name = diff_name.strip()
            if diff_name == "":
                messages.error(request, "難易度名を入力してください")
                return redirect("ctf:manager_question", contest_id=contest.id)
            if len(diff_name) > 32:
                messages.error(request, "難易度名は32文字以下で入力してください")
                return redirect("ctf:manager_question", contest_id=contest.id)
            difficulty = Difficulty(name=diff_name)
            difficulty.save()
            messages.success(request, "難易度を作成しました")
        except Exception:
            messages.error(request, "難易度の作成に失敗しました")
        return redirect("ctf:manager_question", contest_id=contest.id)

    return redirect("ctf:manager_question", contest_id=contest.id)


@login_required
def manager_question_edit_view(
    request: HttpRequest, contest_id: str, question_id: str
):
    contest = get_object_or_404(Contest, id=contest_id)
    cu = ContestUtils(contest)

    if not request.user.is_admin:
        return redirect("ctf:home", contest_id=contest.id)
    if request.method != "POST":
        return redirect("ctf:manager_question", contest_id=contest.id)
    ctx = cu.set_initial_context(request)
    if ctx["player"] is None:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")

    question = get_object_or_404(Question, id=question_id)

    # 値の取得
    try:
        title = request.POST.get("title")
        description = request.POST.get("description")
        flag = request.POST.get("flag")
        point = request.POST.get("point")
        category = request.POST.get("category")
        difficulty = request.POST.get("difficulty")
        is_open = request.POST.get("is_open") == "True"
    except Exception:
        messages.error(request, "入力内容に誤りがあります")
        return redirect("ctf:manager_question", contest_id=contest.id)
    file = request.FILES.get("file", None)

    # 問題タイトルのチェック
    title = title.strip()
    title = re.sub(r"\s+", " ", title)
    if len(title) < 4 or len(title) > 128:
        messages.error(request, "問題タイトルは4文字以上128文字以下で入力してください")
        return redirect("ctf:manager_question", contest_id=contest.id)

    # フラッグのチェック
    flag = flag.strip()
    flag = re.sub(r"\s+", " ", flag)
    if len(flag) < 4 or len(flag) > 128:
        messages.error(request, "flagは4文字以上128文字以下で入力してください")
        return redirect("ctf:manager_question", contest_id=contest.id)
    if re.search(r"\s+", flag) is not None:
        messages.error(request, "flagに空白文字を入れることはできません")
        return redirect("ctf:manager_question", contest_id=contest.id)

    # ポイントのチェック
    try:
        f = float(point)
    except ValueError:
        messages.error(request, "ポイントは数値で入力してください")
        return redirect("ctf:manager_question", contest_id=contest.id)

    if not f.is_integer():
        messages.error(request, "ポイントは整数で入力してください")
        return redirect("ctf:manager_question", contest_id=contest.id)
    point = int(f)

    if point < 0:
        messages.error(request, "ポイントは0以上で入力してください")
        return redirect("ctf:manager_question", contest_id=contest.id)

    # カテゴリのチェック
    try:
        category = Category.objects.get(pk=int(category))
    except ValueError:
        messages.error(request, "カテゴリの値が不正です")
        return redirect("ctf:manager_question", contest_id=contest.id)

    # 難易度のチェック
    try:
        difficulty = Difficulty.objects.get(pk=int(difficulty))
    except ValueError:
        messages.error(request, "難易度の値が不正です")
        return redirect("ctf:manager_question", contest_id=contest.id)

    # 問題文のチェック
    if description == "":
        description = title

    # 問題の編集
    try:
        question.title = title
        question.description = description
        question.flag = flag
        question.point = point
        question.category = category
        question.difficulty = difficulty
        question.is_open = is_open
        question.save()
        if file is not None:
            path = os.path.join(
                settings.BASE_DIR,
                "static",
                "questions",
                str(question.id),
                file.name,
            )
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                for chunk in file.chunks():
                    f.write(chunk)
                question.file_path = os.path.join(
                    "static", "questions", str(question.id), file.name
                )
                question.save()
    except Exception as e:
        print(e)
        messages.error(request, "問題の編集に失敗しました")
        return redirect("ctf:manager_question", contest_id=contest.id)

    messages.success(request, "問題を編集しました")

    return redirect("ctf:manager_question", contest_id=contest.id)
