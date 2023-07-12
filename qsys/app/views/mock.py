from django.contrib import messages
from django.http import HttpRequest, HttpResponseForbidden
from django.shortcuts import redirect
from app.models.ctf_information import CtfInformation
from app.models.question import CtfQuestion
from app.models.category import CtfQuestionCategory
from app.models.difficulty import CtfQuestionDifficulty
from app.models.app_user import AppUser


def create_mock_questions(request: HttpRequest, count: int):
    """Create Mock Questions."""
    user = request.user
    if not user.is_admin:
        return HttpResponseForbidden()

    ctfs = CtfInformation.objects.filter(is_active=True)
    if not ctfs or ctfs[0] is None:
        messages.error(request, "No Active CTF")
        return redirect("index")
    ctf = ctfs[0]

    for i in range(count):
        q = CtfQuestion(
            category_id=CtfQuestionCategory.objects.all()[0].category_id,
            title=f"Mock Q {i + 1}",
            content=f"Answer is {i + 1}",
            explanation=f"Explanation of {i + 1}",
            point=(i + 1) * 10,
            flag=f"{i + 1}",
            difficulty_id=CtfQuestionDifficulty.objects.all()[0].difficulty_id,
            file_path="",
            is_published=True,
            is_practice=False,
            note="",
        )
        q.save()

        ctf.questions.add(q)

    messages.success(request, f"Created {count} Mock Questions")
    return redirect("index")


def create_mock_user(request: HttpRequest):
    user = request.user
    if not user.is_admin:
        return HttpResponseForbidden()

    # /static/dummy/usernames.csvから名前を読み取る
    with open('static/dummy/usernames.csv', 'r') as f:
        lines = f.readlines()
        for line in lines:
            # 末尾の改行とカンマを削除
            username = line.rstrip('\n').rstrip(',')

            # 既に存在するユーザー名はスキップ
            if AppUser.objects.filter(username=username).exists():
                continue

            user = AppUser.objects.create_user(
                username=username,
                password=AppUser.objects.make_random_password()
            )
            user.save()

    messages.success(request, f"Created {len(lines)} Mock Users")

    return redirect("index")
