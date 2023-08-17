from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from .views.index import index

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
    # CTF
    path("ctf/", include("ctf.urls")),
    # Docs
    path("docs/", include("docs.urls")),
]
