from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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
