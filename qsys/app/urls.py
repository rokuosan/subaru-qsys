from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views.answer_history import answer_history
from .views.sample import sample_view
from .views.mock import create_mock_questions, create_mock_user
from .views.ranking import ranking
from .views.account import account
from .views.index import index
from .views.manager import manager
from .views.manager_user import manager_user
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

    # Ranking
    path("ranking/", ranking, name="ranking"),

    # For admin
    path("manager/", manager, name="manager"),
    path("manager/user/", manager_user, name="manager_user"),
    path("manager/ctf/", manager_ctf, name="manager_ctf"),
    path("answer-history/", answer_history, name="answer_history"),


    # Debug
    path(
        "mock/create/questions/<int:count>/",
        create_mock_questions,
        name="mock",
    ),
    path("mock/create/users/", create_mock_user, name="mock_user"),
    path("sample/", sample_view, name="sample"),
]
