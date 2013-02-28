import datetime

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from polls.models import Poll


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


class PollFactory(object):
    @classmethod
    def create(cls, question, days):
        """
        Creates a poll with a `question` and is published `days` from now.
        """
        return Poll.objects.create(question=question,
            pub_date=timezone.now() + datetime.timedelta(days=days))

    @classmethod
    def create_past_poll(cls, question='Past Poll', days=-30):
        return cls.create(question=question, days=days)

    @classmethod
    def create_future_poll(cls, question='Future Poll', days=30):
        return cls.create(question=question, days=days)

class PollViewTests(TestCase):
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
        If a poll has a pub_date in the past,
        it should be shown on the index page
        """
        PollFactory.create_past_poll()
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past Poll>']
        )

    def test_index_view_with_future_poll(self):
        PollFactory.create_future_poll()
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_index_view_with_future_poll_and_past_poll(self):
        PollFactory.create_future_poll()
        PollFactory.create_past_poll()
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Poll: Past Poll>']
        )

