from django.shortcuts import render


def index(request):
    ctx = {}

    return render(request, "app/index.html", ctx)
