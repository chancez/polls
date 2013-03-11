from django.conf.urls import patterns, url
from django.utils import timezone

from polls.models import Poll
from polls.views import PollDetailView, PollListView

urlpatterns = patterns('',
    url(r'^$', PollListView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', PollDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/results/$', PollDetailView.as_view(
        template_name='polls/results.html'), name='results'),

    url(r'^(?P<poll_id>\d+)/vote/$', 'polls.views.vote', name='vote'),
)
