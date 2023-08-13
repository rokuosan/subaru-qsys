from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ctf.models.contest import Contest
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

    return render(request, "ctf/contest/manager/question.html", ctx)
