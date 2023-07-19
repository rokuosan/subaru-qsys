from django.shortcuts import render

from app.models.ctf_information import CtfInformation


def index(request):
    ctx = {}

    ctf = CtfInformation.objects.filter(is_active=True).first()
    if ctf is not None:
        ctx["ctf"] = ctf

    return render(request, "app/index.html", ctx)
