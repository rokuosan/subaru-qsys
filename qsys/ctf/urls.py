from django.urls import path

from ctf.views.questions import questions_view
from ctf.views.index import index_view


urlpatterns = [
    # Index
    path("", index_view, name="index"),

    # Questions
    path("<str:contest_id>/questions/", questions_view, name="questions"),
]
