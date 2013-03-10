import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now())

    def was_published_recently(self):
        """Returns whether or not the poll was published in the last day"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200, blank=False)

    def __unicode__(self):
        return self.choice_text


class Vote(models.Model):
    voter = models.ForeignKey(User)
    poll = models.ForeignKey(Poll)
    choice = models.ForeignKey(Choice)

    class Meta:
        unique_together = ['poll', 'voter']

    def __unicode__(self):
        return self.choice.choice_text
