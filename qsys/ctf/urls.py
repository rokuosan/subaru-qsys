from django.urls import path

from ctf.views.questions import questions_view
from ctf.views.index import index_view
from ctf.views.manager.contest import manager_contest_view
from ctf.views.contest.home import contest_home_view


app_name = "ctf"


urlpatterns = [
    # Index
    path("", index_view, name="index"),

    # Contest
    path("<str:contest_id>/", contest_home_view, name="home"),
    path("<str:contest_id>/questions/", questions_view, name="questions"),

    # Manager
    path("manager/contest/", manager_contest_view, name="manager_contest"),
]
