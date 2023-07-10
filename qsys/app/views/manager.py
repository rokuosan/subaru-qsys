from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import redirect
from .manager_user import manager_user


@login_required
def manager(_: HttpRequest):
    return redirect(manager_user)
