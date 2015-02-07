from django.db import models
from django.contrib.auth.models import User
from project.utils import IntegerRangeField
from project.constants import PROJECT_STATUS, UNAPPROVED
# Create your models here.

class Project(models.Model):
	project_id=models.AutoField(primary_key=True)
	title = models.CharField(max_length=130)
	summary = models.CharField(max_length=500)
	description = models.TextField(max_length = 1000)
	author=models.ForeignKey(User)
	goal = models.IntegerField(default=1000)
	period = IntegerRangeField(default=7, min_value=7, max_value=60)
	video_url=models.URLField(max_length=1000)
	risks_and_challenges=models.TextField(max_length=4000)
	ordering = models.DecimalField(default=1, max_digits = 2, decimal_places = 2)
	start_date = models.DateTimeField()
	created_date = models.DateTimeField(auto_now_add=True)
	status = models.SmallIntegerField(default=UNAPPROVED, choices=PROJECT_STATUS)
	
	def __unicode__(self):
		return str(self.title)

class ProjectImage(models.Model):
	project = models.ForeignKey(Project, related_name='project_image')
	image = models.ImageField(upload_to='images/')
	ordering = models.DecimalField(default=1, max_digits = 2, decimal_places = 2)

	def __unicode__(self):
		return str(self.project.title)

class Pledge(models.Model):
	user = models.ForeignKey(User, related_name='pledges')
	amount = IntegerRangeField(default=1000, min_value=1000)
	project =  models.ForeignKey(Project, related_name='pledges')
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.project + ' - ' + self.user


class Message(models.Model):
	project = models.ForeignKey(Project, related_name='messages')
	user = models.ForeignKey(User, related_name='messages')
	message = models.TextField(max_length=4000)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.title)
