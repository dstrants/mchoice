from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from django.http import JsonResponse
from .helpers import locate_docxs, import_docxs
from .models import Attempt, Question, Aswer, Choice, Test


def index(request):
    return render(request, "tests/index.html")


@login_required
def start_test(request):
    import random
    existing = request.user.attempt_set.filter(finished=False).exists()
    if existing:
        attempt = request.user.attempt_set.filter(finished=False).last()
    else:
        qset = Question.objects.none()
        questions = Question.objects.all()
        mx = Question.objects.count()
        indexes = random.sample(range(0, mx), 30)
        for i in indexes:
            qset |= Question.objects.filter(id=questions[i].id)
        attempt = Attempt.objects.create(user=request.user)
        attempt.questions.set(qset)
        for q in attempt.questions.all():
            Aswer.objects.create(question=q, attempt=attempt)
    return render(request, "tests/test.html", {'aswers': attempt.aswer_set.all(),
                                               'attempt': attempt})


@login_required
def submit_answer(request):
    ch_id = request.GET.get('ch_id')
    choice = get_object_or_404(Choice, id=int(ch_id))
    an_id = request.GET.get('an_id')
    answer = get_object_or_404(Aswer, pk=int(an_id))
    answer.choice = choice
    answer.save()
    return JsonResponse({'status': 'done'})


@login_required
def finish_test(request):
    at_id = request.GET.get('at_id')
    attempt = get_object_or_404(Attempt, id=at_id)
    attempt.finished = True
    attempt.started_at = str(request.GET.get('start'))
    attempt.ended_at = str(request.GET.get('end'))
    attempt.save()
    attempt.calculate_correct()
    return render(request, 'tests/results.html', {'attempt': attempt})


@login_required
def attempts_list(request):
    attempts = request.user.attempt_set.all()
    return render(request, "tests/attemps.html", {'attempts': attempts})


@login_required
def attempt_detail(request, id):
    attempt = get_object_or_404(Attempt, id=id)
    return render(request, "tests/results.html", {'attempt': attempt})


class CreateNewSource(LoginRequiredMixin, CreateView):
    model = Test
    fields = ['title', 'file']


class DetailSource(LoginRequiredMixin, DetailView):
    model = Test


class ListSourcesView(LoginRequiredMixin, ListView):
    model = Test
