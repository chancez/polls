import datetime

from django.db import models
from django.utils import timezone

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
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.choice_text
