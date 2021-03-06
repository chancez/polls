import datetime
import itertools

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import (render, get_object_or_404, redirect,
                              render_to_response)
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView, ListView
from django.utils import timezone

from polls.models import Poll, Choice, Vote


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    user = request.user
    try:
        Vote.objects.get(voter=user, poll=poll.id)
        message = "You've already voted on this!"
        messages.error(request, message)
    except Vote.DoesNotExist:
        try:
            choice = Choice.objects.get(pk=request.POST['choice'])
            Vote.objects.create(poll=poll, choice=choice, voter=user)
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the poll voting form.
            message = "You didn't select a choice."
            messages.error(request, message)
            return render(request, 'polls/detail.html', {
                'poll': poll
            })
    return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))


class PollDetailView(DetailView):
    template_name = 'polls/detail.html'
    model = Poll
    context_object_name = 'poll'
    queryset = Poll.objects.filter(pub_date__lte=timezone.now)

    def dispatch(self, request, *args, **kwargs):
        """
        If a user has voted in the poll already, redirect to poll results,
        else render the voting detail view.
        """
        user = request.user
        vote = None
        try:
            vote = Vote.objects.get(voter=user, poll=self.kwargs['pk'])
        except Vote.DoesNotExist:
            pass
        else:
            self.template_name = 'polls/results.html'
        return super(PollDetailView, self).dispatch(request, vote=vote,
                                                    *args, **kwargs)


class PollListView(ListView):
    queryset = Poll.objects.filter(pub_date__lte=timezone.now) \
                           .exclude(choice__isnull=True).order_by('-pub_date')
    template_name = 'polls/index.html'
    context_object_name = 'poll_list'

    def get_context_data(self, *args, **kwargs):
        context = super(PollListView, self).get_context_data(*args, **kwargs)
        keyfunc = lambda poll: poll.was_published_recently()
        for k, g in itertools.groupby(context['poll_list'], keyfunc):
            key = 'polls_recent' if k else 'polls_rest'
            context[key] = list(g)
        return context
