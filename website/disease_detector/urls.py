from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
app_name = 'disease_detector'
from . import views

urlpatterns = [
    path("", views.index, name="index"),
] 