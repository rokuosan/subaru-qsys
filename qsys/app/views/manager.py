from app.forms.create_user import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseBadRequest
from django.shortcuts import redirect, render

from .index import index


@login_required
def manager(request: HttpRequest):
    ctx = {}
    ctx["form"] = CreateUserForm()

    return render(request, "app/manager.html", ctx)


@login_required
def manager_create_user(request: HttpRequest):
    if not request.user.is_admin:
        return redirect(index)

    if request.method == "GET":
        ctx = {}
        ctx["form"] = CreateUserForm()

        return render(request, "app/ctf.html", ctx)

    elif request.method == "POST":
        pass

    else:
        return HttpResponseBadRequest()
