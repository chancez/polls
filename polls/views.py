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
    try:
        choice = Choice.objects.get(pk=request.POST['choice'])
        #selected_choice, created = choice.vote_set.get_or_create(
        #    choice=choice, voter=request.user)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': poll,
            'error_message': "You didn't select a choice.",
        })
    else:
        vote, created = Vote.objects.get_or_create(
            poll=poll, voter=request.user, defaults={'choice': choice})
        if not created:
            message = "You've already voted on this!"
            messages.warning(request, message)
        return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))


class PollDetailView(DetailView):
    template_name = 'polls/detail.html'
    model = Poll
    context_object_name = 'poll'

    def dispatch(self, request, *args, **kwargs):
        """
        If a user has voted in the poll already, redirect to poll results,
        else render the voting detail view.
        """
        user = request.user
        if user.is_authenticated():
            try:
                vote = Vote.objects.get(voter=user, poll=self.kwargs['pk'])
            except Vote.DoesNotExist:
                vote = None
        if vote:
            return redirect(reverse('polls:results', args=(vote.poll.id,)))
        else:
            return super(PollDetailView, self).dispatch(request, *args,
                                                        **kwargs)
