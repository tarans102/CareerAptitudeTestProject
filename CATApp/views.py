from CATApp.models import Choice, Question
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "index.html")


def question(request, question_number):
    if question_number == 1:
        request.session.flush()
    question = Question.objects.get(question_number=question_number)
    if question:
        return render(request, "question.html", context={"question": question})
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
    career_dict = {}
    for question in Question.objects.all():
        selectedChoice = Choice.objects.get(
            id=request.session[f"question{question.id}"]
        )
        for career in selectedChoice.career["career"]:
            if career not in career_dict:
                career_dict[career] = 1
            else:
                career_dict[career] += 1

    sorted_dict = {
        k: v
        for k, v in sorted(career_dict.items(), key=lambda item: item[1], reverse=True)
    }
    keys = list(sorted_dict.keys())[0:5]
    new_dict = {key: sorted_dict[key] for key in keys}
    return render(request, "result.html", context={"results": new_dict})
