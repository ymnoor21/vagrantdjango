from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from .models import Question, Choice
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'top_5_questions'

    def get_queryset(self):
        return Question.objects.\
            filter(pub_date__lte=timezone.now()).\
            order_by('-pub_date')[:5]


class DetailsView(generic.DetailView):
    template_name = 'polls/details.html'
    model = Question

    def get_queryset(self):
        return Question.objects.\
            filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'
    model = Question

    def get_queryset(self):
        return Question.objects.\
            filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html', {
            'question': question,
            'error_message': "You didn't select choice",
        })

    selected_choice.votes += 1
    selected_choice.save()

    return HttpResponseRedirect(
        reverse('polls:results', args=[question_id])
    )
