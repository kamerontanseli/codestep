from __future__ import unicode_literals
from django.contrib.auth.models import User 
from django.db import models

# Create your models here.

class Project(models.Model):
	DIFFICULTIES = (
	   	(0, 'Beginner'), 
		(1, 'Adept'), 
		(2, 'Advanced'), 
		(3, 'Expert')
	)
	title = models.CharField(max_length=255)
	description = models.TextField(blank=True)
	cover_image = models.ImageField(upload_to="covers/", blank=True, null=True)
	difficulty = models.IntegerField(choices=DIFFICULTIES)
	def __unicode__(self):
		return self.title 

	def get_steps(self): 
		return self.steps.all().order_by("order")


class Step(models.Model):
	title = models.CharField(max_length=255)
	content = models.TextField(blank=True)
	project = models.ForeignKey('Project', related_name="steps")
	order = models.IntegerField(default=0)
	def __unicode__(self):
		return self.title 

class Progress(models.Model):
	project = models.ForeignKey('Project', related_name="users_progress")
	step = models.IntegerField(default=0)
	user = models.ForeignKey(User, related_name="progress")
	def __unicode__(self):
		return self.user.__unicode__() + " " + self.project.__unicode__()