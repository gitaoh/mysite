from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice


def index(request):
    latest = Question.objects.order_by("-pub_date")[:5]
    # out = ", ".join([q.question_text for q in latest])
    # out = "Hello, world. You're at the polls index."
    context = {
        "latest_question_list": latest
    }
    return render(request, "polls/index.html", context)


def details(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/details.html", {"question": question})


def results(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {"question": q})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.choice_set.get(pk=request.POST.get("choice"))
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form
        ctx = {"question": question,
               "error_message": "you didn't select a choice"}
        return render(request, "polls/details.html", ctx)
    else:
        choice.votes += 1
        choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
