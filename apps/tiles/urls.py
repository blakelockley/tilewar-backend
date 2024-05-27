# type: ignore
from django.urls import path

from . import views

urlpatterns = [
    path("tiles/", views.TilesViews.as_view()),
]
