from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from ctf.models.contest import Contest
from ctf.utils.contest_util import ContestUtils
from app.models.app_user import AppUser


@login_required
def manager_player_view(request: HttpRequest, contest_id: str):
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    cu = ContestUtils(contest)

    if not request.user.is_admin:
        return redirect("ctf:home", contest_id=contest.id)

    # 公開設定
    fun = cu.get_page_protection(request)
    if fun is not None:
        return fun[0](*fun[1], **fun[2])

    # コンテキストの初期化
    ctx = cu.set_initial_context(request)
    if ctx["player"] is None:
        messages.info(request, "このコンテストに参加していません")
        return redirect("ctf:index")
    ctx["msg"] = "このページでは、プレイヤーに関する操作を行うことができます。ユーザとプレイヤーについてはドキュメントを参照してください。"

    players = cu.get_players()
    ctx["players"] = players

    all_players = cu.get_players(all=True)
    ctx["all_players"] = all_players

    users = AppUser.objects.filter(player__isnull=True)
    ctx["users"] = users

    return render(request, "ctf/contest/manager/player.html", ctx)


@login_required
def create_player_view(request: HttpRequest, contest_id: str):
    contest: Contest = get_object_or_404(Contest, id=contest_id)
    cu = ContestUtils(contest)

    # 拒否
    if not request.user.is_admin:
        return redirect("ctf:home", contest_id=contest.id)
    if request.method != "POST":
        return redirect("ctf:manager_player", contest_id=contest.id)

    create_type = request.POST.get("create_type")
    if create_type is None:
        # ユーザの取得
        user = cu.get_user(request.POST.get("user_id"))
        if user is None:
            messages.error(request, "ユーザが存在しません")
            return redirect("ctf:manager_player", contest_id=contest.id)

        # プレイヤーの作成
        name = request.POST.get("name")
        if name is None or name == "":
            name = user.username
        player = cu.create_player(user, name)

        # メッセージの設定
        if player is None:
            messages.error(request, "プレイヤーの作成に失敗しました")
        else:
            messages.success(request, "プレイヤーを作成しました")
    elif create_type == "user":
        username = request.POST.get("username")
        password = request.POST.get("password")
        is_admin = request.POST.get("is_admin") == "True"
        if username is None or username == "":
            messages.error(request, "ユーザ名を入力してください")
            return redirect("ctf:manager_player", contest_id=contest.id)
        if password is None or password == "":
            messages.error(request, "パスワードを入力してください")
            return redirect("ctf:manager_player", contest_id=contest.id)

        user = cu.create_user(username, password, is_admin)
        if user is None:
            messages.error(request, "ユーザの作成に失敗しました")
            return redirect("ctf:manager_player", contest_id=contest.id)

        messages.success(request, "ユーザを作成しました")

    return redirect("ctf:manager_player", contest_id=contest.id)
