from django.urls import path

from ctf.views.contest.questions import question_detail_view, questions_view
from ctf.views.index import index_view
from ctf.views.contest.manager.contest import manager_contest_view
from ctf.views.contest.manager.team import manager_team_view
from ctf.views.contest.home import contest_home_view
from ctf.views.contest.account import account_view
from ctf.views.contest.ranking import ranking_view
from ctf.views.contest.monitor.stats import stats_view
from ctf.views.contest.monitor.answer import answer_view


app_name = "ctf"


urlpatterns = [
    # Index
    path("", index_view, name="index"),
    # Contest
    path("<str:contest_id>/", contest_home_view, name="home"),
    path("<str:contest_id>/questions/", questions_view, name="questions"),
    path(
        "<str:contest_id>/questions/<str:question_id>",
        question_detail_view,
        name="question_detail",
    ),
    path("<str:contest_id>/account/", account_view, name="account"),
    path("<str:contest_id>/ranking/", ranking_view, name="ranking"),
    # Manager
    path(
        "<str:contest_id>/manager/contest/",
        manager_contest_view,
        name="manager_contest",
    ),
    path(
        "<str:contest_id>/manager/team/",
        manager_team_view,
        name="manager_team",
    ),
    # Monitor
    path(
        "<str:contest_id>/monitor/stats/",
        stats_view,
        name="stats",
    ),
    path("<str:contest_id>/monitor/answer/", answer_view, name="answer"),
]
