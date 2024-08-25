from django.urls import path

from . import views

app_name = "CATApp"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_number>/question/", views.question, name="question"),
    path("results/", views.results, name="results"),
    path("<int:question_number>/answer/", views.answer, name="answer"),
    path(
        "retrieveQuestionDatabase",
        views.retrieveQuestionDatabase,
        name="retrieveQuestionDatabase",
    ),
    path(
        "retrieveChoiceDatabase",
        views.retrieveChoiceDatabase,
        name="retrieveChoiceDatabase",
    ),
    path(
        "retrieveResponseDatabase",
        views.retrieveResponseDatabase,
        name="retrieveResponseDatabase",
    ),
    path(
        "updateQuestionDatabase",
        views.updateQuestionDatabase,
        name="updateQuestionDatabase",
    ),
    path(
        "updateChoiceDatabase",
        views.updateChoiceDatabase,
        name="updateChoiceDatabase",
    ),
    path(
        "updateResponseDatabase",
        views.updateResponseDatabase,
        name="updateResponseDatabase",
    ),
]
