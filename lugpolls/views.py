from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from polls.models import Vote


def home(request):
    return render(request, 'index.html', {})


@login_required()
def profile(request):
    votes = Vote.objects.filter(voter=request.user) \
                        .prefetch_related() \
                        .order_by('-vote_date')
    return render(request, 'users/profile.html', {'votes': votes})
