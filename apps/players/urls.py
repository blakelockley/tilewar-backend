# type: ignore
from django.urls import path

from . import views

urlpatterns = [
    path("me/", views.WhoAmIView.as_view()),
    path("teams/", views.TeamsView.as_view()),
]
