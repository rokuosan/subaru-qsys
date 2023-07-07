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

    ctx = {}

    ctfs = CtfInformation.objects.all()

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
