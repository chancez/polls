from django.conf.urls import patterns, url
from django.views.generic import DetailView
from django.utils import timezone

from polls.models import Poll
from polls.views import PollDetailView, PollListView

urlpatterns = patterns('',
    url(r'^$', PollListView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', DetailView.as_view(
        queryset=Poll.objects.filter(pub_date__lte=timezone.now),
        model=Poll, template_name='polls/results.html'), name='results'),

    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote', name='vote'),
)
