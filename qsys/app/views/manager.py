import random

from app.forms.create_user import CreateUserForm
from app.models.app_user import AppUser
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
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

        return render(request, "app/manager.html", ctx)

    elif request.method == "POST":
        usernames = request.POST.get("usernames")
        if usernames is None:
            print("OK")
        else:
            users = [name.strip() for name in usernames.splitlines() if name]
            users_set = []
            users_set.append("username, password")
            for user in users:
                if AppUser.objects.filter(username=user).exists():
                    continue

                password = AppUser.objects.make_random_password()
                AppUser.objects.create_user(username=user, password=password)
                users_set.append("{}, {}".format(user, password))

            # Return users_set as csv
            csv = "\n".join(users_set)
            rand = random.randrange(1000, 10000)
            response = HttpResponse(csv, content_type="text/csv")
            content = f'attachment; filename="users-{rand}.csv"'
            response["Content-Disposition"] = content
            return response

        return redirect(manager_create_user)

    else:
        return HttpResponseBadRequest()
