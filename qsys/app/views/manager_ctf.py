from datetime import datetime
from django.utils import timezone
from django.http import HttpRequest
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.views.index import index
from app.models.ctf_information import CtfInformation


@login_required
def manager_ctf(request: HttpRequest):
    user = request.user
    if not user.is_admin:
        messages.info(request, "管理者権限が必要です")
        return redirect(index)

    if request.method == "GET":
        ctx = {}
        ctx["ctfs"] = []

        # CTX MODEL
        # ctx["ctfs"] = [
        #     {
        #         "type": running,
        #         "ctfs": [
        #            {
        #               "name": "CTF_NAME",
        #               "id": 1,
        #               "start_at": "2021-01-01 00:00:00",
        #               "end_at": "2021-01-01 00:00:00",
        #            },
        #         ]
        #     },
        #     {
        #         "type": stopped,
        #         "ctfs": [
        #            {
        #               "name": "CTF_NAME",
        #               "id": 1,
        #               "start_at": "2021-01-01 00:00:00",
        #               "end_at": "2021-01-01 00:00:00",
        #            },
        #         ]
        #     },
        # ]

        # セッションからのメッセージを表示
        if "message" in request.session:
            msg = request.session["message"]
            messages.add_message(request, msg["type"], msg["text"])
            del request.session["message"]

        ctfs = CtfInformation.objects.all()
        ctx["all"] = ctfs

        # 実行中のCTFを取得
        running_ctfs = ctfs.filter(is_active=True)
        # ほとんどの場合、実行中のCTFは1つだけだが、人為的ミスで複数ある場合がある
        # 実行中のCTFが複数ある場合は、経過時間が長いCTFを優先する
        if running_ctfs.count() > 1:
            # 進行した時間が長いCTFを優先する
            running_ctfs = running_ctfs.order_by("start_at")
            # それ以外のCTFは停止する
            for ctf in running_ctfs[1:]:
                ctf.is_active = False
                ctf.save()

        ctx["ctfs"].append(
            {
                "type": "running",
                "category": "開催中のCTF",
                "ctfs": running_ctfs,
            }
        )

        # 停止中のCTFを取得
        stopped_ctfs = ctfs.filter(is_active=False)
        ctx["ctfs"].append(
            {
                "type": "stopped",
                "category": "開催前・開催後のCTF",
                "ctfs": stopped_ctfs,
            }
        )

        return render(request, "app/manager_ctf.html", ctx)

    elif request.method == "POST":
        if "stop" in request.POST:
            ctf_id = request.POST.get("id")
            ctf = CtfInformation.objects.get(pk=ctf_id)
            ctf.end_at = datetime.now(timezone.utc)
            ctf.is_active = False
            ctf.is_paused = True
            ctf.save()
            request.session["message"] = {
                "type": messages.WARNING,
                "text": f"[{ctf.name}]を終了しました",
            }
        elif "pause" in request.POST:
            ctf_id = request.POST.get("id")
            ctf = CtfInformation.objects.get(pk=ctf_id)
            ctf.is_paused = True
            ctf.save()
            request.session["message"] = {
                "type": messages.WARNING,
                "text": f"[{ctf.name}]を一時停止しました",
            }
        elif "restart" in request.POST:
            ctf_id = request.POST.get("id")
            ctf = CtfInformation.objects.get(pk=ctf_id)

            active_ctfs = CtfInformation.objects.filter(is_active=True)
            if active_ctfs.exists():
                request.session["message"] = {
                    "type": messages.ERROR,
                    "text": "CTFを同時開催することはできません",
                }
                return redirect(manager_ctf)

            ctf.start_at = datetime.now(timezone.utc)
            ctf.end_at = datetime.now(timezone.utc) + timezone.timedelta(
                hours=2
            )
            ctf.is_active = True
            ctf.save()
            request.session["message"] = {
                "type": messages.INFO,
                "text": f"[{ctf.name}]を再実施しました",
            }
        elif "resume" in request.POST:
            ctf_id = request.POST.get("id")
            ctf = CtfInformation.objects.get(pk=ctf_id)
            ctf.is_paused = False
            ctf.save()
            request.session["message"] = {
                "type": messages.SUCCESS,
                "text": f"[{ctf.name}]を再開しました",
            }

        return redirect(manager_ctf)

    return redirect(index)
