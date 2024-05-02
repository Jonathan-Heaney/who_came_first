from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("check-answer/", views.check_answer, name='check-answer')
]
