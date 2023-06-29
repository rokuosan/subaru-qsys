from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views.index import index
from .views.questions import questions


urlpatterns = [
    path('', index, name='index'),

    # Login/Logout
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(
        redirect_authenticated_user=True,
        template_name='app/login.html'
    ), name='login'),

    # Questions
    path('questions/', questions, name='questions'),
]
