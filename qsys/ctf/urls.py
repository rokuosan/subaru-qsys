from django.urls import path

from ctf.views.questions import questions_view


urlpatterns = [
    path('<str:contest_id>/questions/', questions_view, name='questions'),
]
