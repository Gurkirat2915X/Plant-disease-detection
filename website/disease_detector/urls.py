from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = "disease_detector"
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("model_intro", views.model_intro, name="model_intro"),
    path("team", views.team, name="team"),
    path("detect", views.detect, name="detect"),
    path("result/<int:id>", views.result, name="result"),
    path("chat", views.chat, name="chat"),
]
