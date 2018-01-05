import math

from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from django.utils.text import Truncator
from django.contrib.auth.models import AbstractUser


from markdown import markdown

class ShiftManager(models.Manager):
	def most_recent(self):
		return self.order_by('-start_datetime')

	def create_shift(self, start_datetime, end_datetime): # creating model instance
		shift = self.create(start_datetime = runs_start, end_datetime = runs_end)
		return shift

class GroupShift(models.Model):
    name = models.CharField(max_length=30, unique=True)
    group_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100)
    objects = ShiftManager()

    def __str__(self):
        return self.name or ''


class Shift(models.Model):
    shifts_text = models.CharField(max_length=200)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    groupshift = models.ForeignKey(GroupShift, related_name='shifts')
    starter = models.ForeignKey(User, related_name='shifts')
    views = models.PositiveIntegerField(default=0)
    users = models.ManyToManyField(User, related_name='users')
    objects = ShiftManager()

    def __str__(self):
        return self.shifts_text

    def get_runs_count(self):
        count = self.runs.count()
        return count


class Run(models.Model):
    runs_text = models.CharField(max_length=200)
    message = models.TextField(max_length=4000, null=True)
    shift = models.ForeignKey(Shift, related_name='runs')
    runs_start = models.DateTimeField(blank=True, null=True)
    runs_end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='runs')
    updated_by = models.ForeignKey(User, null=True, related_name='+')
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.runs_text
