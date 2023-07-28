from django.http import HttpRequest
from django.shortcuts import render


def result(request: HttpRequest):
    return render(request, "app/result.html")
