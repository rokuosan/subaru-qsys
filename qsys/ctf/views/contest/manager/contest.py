from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone

from ctf.models.contest import Contest
from ctf.utils.contest_util import ContestUtils


@login_required
def manager_contest_view(request: HttpRequest, contest_id: str):
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    cu = ContestUtils(contest)

    if not request.user.is_admin:
        return redirect("ctf:home", contest_id=contest.id)

    # コンテキストの初期化
    ctx = cu.set_initial_context(request)
    if ctx["player"] is None:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")
    ctx["msg"] = (
        "このページでは、コンテストに関する情報を確認・編集することができます。"
        + "プレイヤー・チーム・問題などの追加・編集・削除については各マネージャーにて行ってください。"
    )
    status_table = {
        "preparing": ("準備中", "info", "preparing"),
        "running": ("開催中", "success", "running"),
        "finished": ("終了", "danger", "finished"),
        "paused": ("一時停止中", "warning", "paused"),
    }
    ctx["status_table"] = [
        (s, status_table[s][0]) for s in status_table.keys()
    ]
    ctx["status"] = status_table[contest.status]
    ctx["is_open"] = contest.is_open

    # コンテスト情報を集計する
    # 集計内容は以下に示す
    # - プレイヤー数
    # - チーム数
    # - 問題数
    # - 開催期間

    # プレイヤー数
    player_count = ("参加者数", len(cu.get_players()))

    # チーム数
    team_count = ("チーム数", contest.teams.count())

    # 問題数
    problem_count = ("登録問題数", contest.questions.count())

    # 開催期間
    start_time = contest.start_at
    end_time = contest.end_at
    duration = ("開催時間", end_time - start_time)
    now = timezone.now()
    if start_time > now:
        time_status = "開催前"
    elif end_time < now:
        time_status = "開催期間超過"
    else:
        time_status = "開催期間内"

    # 集計結果をコンテキストに追加
    ctx["contest_info"] = [
        ("コンテスト名", contest.name),
        ("コンテストID", contest.id),
        ("開催状況", time_status),
        ("公開状況", "公開中" if contest.is_open else "非公開"),
        player_count,
        team_count,
        problem_count,
        duration,
    ]

    return render(request, "ctf/contest/manager/contest.html", ctx)


@login_required
def manager_contest_update_view(request: HttpRequest, contest_id: str):
    """コンテストの開催状況を更新するView"""

    contest: Contest = get_object_or_404(Contest, id=contest_id)
    cu = ContestUtils(contest)
    if not request.user.is_admin:
        return redirect("ctf:home", contest_id=contest.id)
    ctx = cu.set_initial_context(request)
    if ctx["player"] is None:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")
    if request.method != "POST":
        return redirect("ctf:manager_contest", contest_id=contest.id)

    update_type = request.POST.get("update_type")
    if update_type is None:
        messages.error(request, "不正なリクエストです")
        return redirect("ctf:manager_contest", contest_id=contest.id)

    # リクエスト処理
    if update_type == "status":
        # コンテストの開催状況を更新する
        status = request.POST.get("status")
        if status not in ["preparing", "running", "finished", "paused"]:
            messages.error(request, "不正なリクエストです")
            return redirect("ctf:manager_contest", contest_id=contest.id)

        contest.status = status
        contest.save()
        messages.success(request, "コンテストの開催状況を更新しました")
        return redirect("ctf:manager_contest", contest_id=contest.id)
    elif update_type == "visibility":
        # コンテストの可視性を更新する
        visibility = request.POST.get("visibility")
        if visibility == "on":
            contest.is_open = True
        else:
            contest.is_open = False
        contest.save()
        messages.success(request, "コンテストの可視性を更新しました")
        return redirect("ctf:manager_contest", contest_id=contest.id)

    return redirect("ctf:manager_contest", contest_id=contest.id)
