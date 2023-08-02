from django.utils import timezone
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.views.index import index
from ctf.models.contest import Contest


@login_required
def manager_ctf(request: HttpRequest):
    user = request.user
    if not user.is_admin:
        messages.info(request, "管理者権限が必要です")
        return redirect(index)

    if request.method == "GET":
        ctx = {}
        ctx["contests"] = []

        contests = Contest.objects.all()
        ctx["all_contests"] = contests

        # 実行中のCTFを取得
        running_contests = Contest.get_active_contests()
        if running_contests.count() > 1:
            running_contests = running_contests.order_by("start_at")
            for contest in running_contests[1:]:
                contest.set_status("finished")
                contest.save()

        running_contests = Contest.get_active_contests()
        status = None
        for c in running_contests:
            if c.is_over:
                status = {"type": "danger", "msg": "開催期間終了"}

        ctx["contests"].append(
            {
                "type": "running",
                "status": status,
                "category": "開催中のコンテスト",
                "contests": running_contests,
            }
        )

        # 停止中のCTFを取得
        closed_contests = Contest.get_closed_contests()
        ctx["contests"].append(
            {
                "type": "closed",
                "category": "開催前・開催後のコンテスト",
                "contests": closed_contests,
            }
        )

        return render(request, "app/manager_ctf.html", ctx)

    elif request.method == "POST":
        if "stop" in request.POST:
            contest_id = request.POST.get("id")
            contest = Contest.objects.get(pk=contest_id)
            contest.status = "finished"
            contest.save()
            messages.warning(request, f"[{contest.name}]を終了しました")
        elif "pause" in request.POST:
            contest_id = request.POST.get("id")
            contest = Contest.objects.get(pk=contest_id)
            contest.status = "paused"
            contest.save()
            messages.warning(request, f"[{contest.name}]を一時停止しました")
        elif "restart" in request.POST:
            contest_id = request.POST.get("id")
            contest = Contest.objects.get(pk=contest_id)

            active_contests = Contest.get_active_contests()
            if active_contests.exists():
                messages.error(request, "CTFを同時開催することはできません")
                return redirect(manager_ctf)
            contest.status = "paused"
            contest.start_at = timezone.now()
            contest.end_at = timezone.now() + timezone.timedelta(hours=2)
            contest.save()
            messages.success(request, f"[{contest.name}]を再実施しました")
        elif "resume" in request.POST:
            contest_id = request.POST.get("id")
            contest = Contest.objects.get(pk=contest_id)
            contest.status = "running"
            contest.save()
            messages.info(request, f"[{contest.name}]を再開しました")

        return redirect(manager_ctf)

    return redirect(index)
