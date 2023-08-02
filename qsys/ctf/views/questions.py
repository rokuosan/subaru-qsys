from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.shortcuts import render

from ctf.models.contenst import Contest


@login_required
def questions_view(request: HttpRequest, contest_id: str):
    """開催しているCTFで公開中の問題を表示するView"""
    contest: Contest = get_object_or_404(Contest, id=contest_id)

    return HttpResponse("Success, " + contest.id)


@login_required
def question(request: HttpRequest, contest_name: str, question_id: int):
    """開催しているCTFで公開中の問題を表示するView"""
    pass
