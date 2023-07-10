import random

from app.forms.create_user import CreateUserForm
from app.models.app_user import AppUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render

from .index import index


@login_required
def manager_user(request: HttpRequest):
    if not request.user.is_admin:
        return redirect(index)

    if request.method == "GET":
        ctx = {}
        ctx["form"] = CreateUserForm()

        # Set session message to messages
        if "message" in request.session:
            messages.add_message(
                request, request.session["level"], request.session["message"])
            del request.session["message"]
            del request.session["level"]

        return render(request, "app/manager_user.html", ctx)

    elif request.method == "POST":
        usernames = request.POST.get("usernames")
        if usernames is None:
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_admin = request.POST.get("is_admin") == "on"
                user.set_password(form.cleaned_data["password"])
                user.save()

                # Set success message to session
                username = form.cleaned_data["name"]
                request.session["message"] = f"ユーザー[ {username} ]を作成しました。"
                request.session["level"] = messages.SUCCESS

                return redirect(manager_user)
            else:
                request.session["message"] = "ユーザーの作成に失敗しました。"
                request.session["level"] = messages.ERROR

                return redirect(manager_user)
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

        return redirect(manager_user)

    else:
        return HttpResponseBadRequest()
