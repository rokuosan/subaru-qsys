from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from app.views.index import index


@login_required
def manager_ctf(request: HttpRequest):
    user = request.user
    if not user.is_admin:
        return redirect(index)

    return redirect(index)
