from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views.account import account
from .views.index import index
from .views.manager import manager, manager_user
from .views.manager_ctf import manager_ctf
from .views.questions import question_detail, questions

urlpatterns = [
    path("", index, name="index"),
    # Login/Logout
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "login/",
        LoginView.as_view(
            redirect_authenticated_user=True, template_name="app/login.html"
        ),
        name="login",
    ),
    # Questions
    path("questions/", questions, name="questions"),
    path(
        "questions/<int:question_id>/", question_detail, name="question_detail"
    ),
    # Account
    path("account/", account, name="account"),
    # For admin
    path("manager/", manager, name="manager"),
    path("manager/user/", manager_user, name="manager_user"),
    path("manager/ctf/", manager_ctf, name="manager_ctf"),
]
