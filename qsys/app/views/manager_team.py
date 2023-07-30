from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def manager_team(request):
    return render(request, "app/manager_team.html")
