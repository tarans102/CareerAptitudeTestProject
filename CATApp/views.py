import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from CATApp.models import Choice, Question, Response


# Create your views here.
def index(request):
    return render(request, "index.html")


def question(request, question_number):
    if question_number == 1:
        request.session.flush()
        request.session["username"] = request.POST["name"]
    question = Question.objects.get(question_number=question_number)
    if question:
        return render(
            request,
            "question.html",
            context={
                "question": question,
                "numQuestions": len(Question.objects.all()),
            },
        )
    else:
        return results(request)


def answer(request, question_number):
    q = Question.objects.get(question_number=question_number)
    choice_id = request.POST[f"choice{q.id}"]
    c = Choice.objects.get(id=choice_id)
    qLength = len(Question.objects.all())

    request.session[f"question{q.id}"] = choice_id

    if question_number == qLength:
        return HttpResponseRedirect("/CATApp/results/")
        # return results(request)
    return HttpResponseRedirect(f"/CATApp/{question_number+1}/question/")
    # return question(request, question_id + 1)


def results(request):
    response_dict = {}
    career_dict = {}
    for question in Question.objects.all():
        selectedChoice = Choice.objects.get(
            id=request.session[f"question{question.id}"]
        )
        response_dict[question.id] = selectedChoice.id

        for career in selectedChoice.career["career"]:
            if career not in career_dict:
                career_dict[career] = 1
            else:
                career_dict[career] += 1

    career_dict_sorted = {
        k: v
        for k, v in sorted(career_dict.items(), key=lambda item: item[1], reverse=True)
    }
    Response.objects.create(
        username=request.session["username"],
        response=response_dict,
        results=career_dict_sorted,
    )
    keys = list(career_dict_sorted.keys())[0:5]
    career_dict_short = {key: career_dict_sorted[key] for key in keys}
    return render(
        request,
        "result.html",
        context={
            "results": career_dict_short,
            "username": request.session["username"],
        },
    )


@login_required
@permission_required("CATApp.retrieveDatabase", raise_exception=True)
def retrieveQuestionDatabase(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename = "database.json"'
    allQuestions = Question.objects.all()
    questionsDict = {}
    for question in allQuestions:
        questionsDict[question.id] = {
            "question_number": question.question_number,
            "question_text": question.question_text,
        }

    questionsFile = open("questions.json", "w")
    questionsFile.write(json.dumps(questionsDict, indent=4))
    return render(
        request,
        "database.html",
        context={"database": json.dumps(questionsDict, indent=4)},
    )


@login_required
@permission_required("CATApp.retrieveDatabase", raise_exception=True)
def retrieveChoiceDatabase(request):
    allChoices = Choice.objects.all()
    choicesDict = {}
    for choice in allChoices:
        choicesDict[choice.id] = {
            "question": choice.question.id,
            "choice_text": choice.choice_text,
            "career": choice.career,
        }
    choicesFile = open("choices.json", "w")
    choicesFile.write(json.dumps(choicesDict, indent=4))
    return render(
        request,
        "database.html",
        context={"database": json.dumps(choicesDict, indent=4)},
    )


@login_required
@permission_required("CATApp.retrieveDatabase", raise_exception=True)
def retrieveResponseDatabase(request):
    allResponses = Response.objects.all()
    responsesDict = {}
    for response in allResponses:
        responsesDict[response.id] = {
            "username": response.username,
            "response": response.response,
            "results": response.results,
        }
    responsesFile = open("responses.json", "w")
    responsesFile.write(json.dumps(responsesDict, indent=4))
    return render(
        request,
        "database.html",
        context={"database": json.dumps(responsesDict, indent=4)},
    )


@login_required
@permission_required("CATApp.retrieveDatabase", raise_exception=True)
def updateQuestionDatabase(request):
    questionFile = open("questions.json", "r")
    questionDict = json.loads(questionFile.read())

    for i in questionDict.keys():
        try:
            question = Choice.objects.get(id=int(i))
            question.question_number = questionDict[i]["question_number"]
            question.question_text = questionDict[i]["question_text"]
        except ObjectDoesNotExist:
            print("Not found. Will create")
            Question.objects.create(
                question_number=questionDict[i]["question_number"],
                question_text=questionDict[i]["question_text"],
            )

    return render(request, "database.html", context={"database": questionDict})


@login_required
@permission_required("CATApp.retrieveDatabase", raise_exception=True)
def updateChoiceDatabase(request):
    choiceFile = open("choices.json", "r")
    choiceDict = json.loads(choiceFile.read())

    for i in choiceDict.keys():
        try:
            choice = Choice.objects.get(id=int(i))
            choice.question_id = choiceDict[i]["question"]
            choice.choice_text = choiceDict[i]["choice_text"]
            choice.career = choiceDict[i]["career"]
        except ObjectDoesNotExist:
            print("Not found. Will create")
            Choice.objects.create(
                question_id=choiceDict[i]["question"],
                choice_text=choiceDict[i]["choice_text"],
                career=choiceDict[i]["career"],
            )

    return render(request, "database.html", context={"database": choiceDict})


@login_required
@permission_required("CATApp.retrieveDatabase", raise_exception=True)
def updateResponseDatabase(request):
    responseFile = open("responses.json", "r")
    responseDict = json.loads(responseFile.read())

    for i in responseDict.keys():
        try:
            response = Response.objects.get(id=int(i))
            response.username = responseDict[i]["username"]
            response.response = responseDict[i]["response"]
            response.results = responseDict[i]["results"]
        except ObjectDoesNotExist:
            print("Not found. Will create")
            Response.objects.create(
                username=responseDict[i]["username"],
                response=responseDict[i]["response"],
                results=responseDict[i]["results"],
            )

    return render(request, "database.html", context={"database": responseDict})
