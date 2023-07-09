from datetime import datetime
from django.utils import timezone
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from app.views.index import index
from app.models.ctf_information import CtfInformation


@login_required
def manager_ctf(request: HttpRequest):
    user = request.user
    if not user.is_admin:
        return redirect(index)

    if request.method == "GET":
        ctx = {}

        ctfs = CtfInformation.objects.all()
        ctx["ctfs"] = ctfs

        now = datetime.now(timezone.utc)

        upcoming_ctf = ctfs.filter(start_at__gte=now)
        if upcoming_ctf.exists():
            ctx["upcoming"] = upcoming_ctf

        past_ctf = ctfs.filter(end_at__lte=now)
        if past_ctf.exists():
            ctx["past"] = past_ctf

        current_ctf = ctfs.filter(start_at__lte=now, end_at__gte=now)
        if current_ctf.exists():
            ctx["current"] = current_ctf

        return render(request, "app/manager_ctf.html", ctx)

    elif request.method == "POST":
        if "start" in request.POST:
            ctf_id = request.POST.get("id")
            ctf = CtfInformation.objects.get(pk=ctf_id)
            ctf.is_active = True
            ctf.save()
        elif "stop" in request.POST:
            ctf_id = request.POST.get("id")
            ctf = CtfInformation.objects.get(pk=ctf_id)
            ctf.end_at = datetime.now(timezone.utc)
            ctf.is_active = False
            ctf.save()
        elif "pause" in request.POST:
            ctf_id = request.POST.get("id")
            ctf = CtfInformation.objects.get(pk=ctf_id)
            ctf.is_active = False
            ctf.save()
        elif "restart" in request.POST:
            ctf_id = request.POST.get("id")
            ctf = CtfInformation.objects.get(pk=ctf_id)
            ctf.start_at = datetime.now(timezone.utc)
            ctf.end_at = datetime.now(timezone.utc) + timezone.timedelta(
                hours=2
            )
            ctf.is_active = True
            ctf.save()

        return redirect(manager_ctf)

    return redirect(index)
