import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from polls.models import Poll, Choice


class PollMethodTests(TestCase):

    def test_was_published_recently(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future
        """
        future_poll = Poll(pub_date=timezone.now() +
                           datetime.timedelta(days=30))
        self.assertEqual(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_old_poll(self):
        """
        was_published_recently() should return false for
        polls older than 1 day
        """
        old_poll = Poll(pub_date=timezone.now() -
                        datetime.timedelta(days=30))

        self.assertEqual(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """
        was_published_recently() should return true for
        polls published in the last day
        """
        recent_poll = Poll(pub_date=timezone.now() -
                           datetime.timedelta(hours=1))
        self.assertEqual(recent_poll.was_published_recently(), True)


def create_poll(question, days, choices=True):
    """
    Creates a poll with a `question` and is published `days` from now.
    If choices evaluates to true, then we create a poll with 2 choices
    """

    pub_date = timezone.now() + datetime.timedelta(days=days)
    poll = Poll.objects.create(question=question, pub_date=pub_date)
    if choices:
        create_choice(poll, 2)
    return poll


def create_past_poll(question='Past Poll', days=-30, *args, **kwargs):
    return create_poll(question=question, days=days, *args, **kwargs)


def create_future_poll(question='Future Poll', days=30, *args, **kwargs):
    return create_poll(question=question, days=days, *args, **kwargs)


def create_choice(Poll, n=1, *args, **kwargs):
    """
    Creates `n` Choice models with their choice set to `Poll`.
    If `text` is specified, the Choice models with choice_text set to `text`.
    """
    text = kwargs.get('text', "TestChoice")
    for i in xrange(1, n+1):
        if "TestChoice" in text:
            text += str(i)
        Choice.objects.create(choice_text=text, poll=Poll)


class PollIndexViewTests(TestCase):
    def test_index_view_with_no_polls(self):
        """
        If no polls exist, a message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_past_poll(self):
        """
        If a poll has a pub_date in the past, and contains choices
        it should be shown on the index page
        """
        create_past_poll()
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past Poll>']
        )

    def test_index_view_with_future_poll(self):
        create_future_poll()
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_future_poll_and_past_poll(self):
        create_future_poll()
        create_past_poll()
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past Poll>']
        )

    def test_index_view_with_multi_past_polls(self):
        create_poll(question='Past Poll 1', days=-10)
        create_poll(question='Past Poll 2', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            # Order matters
            ['<Poll: Past Poll 2>', '<Poll: Past Poll 1>']
        )

    def test_index_view_polls_without_choices(self):
        """The index view should not show polls without choices"""
        poll = create_past_poll(choices=False)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])


class PollDetailViewTests(TestCase):
    def test_detail_view_with_future_poll(self):
        future_poll = create_future_poll()
        response = self.client.get(reverse('polls:detail',
                                   args=(future_poll.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_past_poll(self):
        past_poll = create_past_poll()
        response = self.client.get(reverse('polls:detail',
                                   args=(past_poll.id,)))
        self.assertEqual(response.status_code, 200)
