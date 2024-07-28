from django.urls import path

from . import views

app_name = "CATApp"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_number>/question/", views.question, name="question"),
    path("results/", views.results, name="results"),
    path("<int:question_number>/answer/", views.answer, name="answer"),
]
