from django.db import models
from django.contrib.auth.models import User
from project.utils import IntegerRangeField
from project.constants import PROJECT_STATUS, UNAPPROVED
from math import floor
# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=30)
    summary = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    author = models.ForeignKey(User)
    goal = IntegerRangeField(default=20000, min_value=20000, max_value=200000)
    period = IntegerRangeField(default=5, min_value=5, max_value=45)
    video_url = models.URLField(max_length=1000, blank=True)
    team = models.TextField(max_length=1000)
    risks_and_challenges = models.TextField(max_length=4000, blank=True)
    ordering = models.DecimalField(default=1, max_digits=4, decimal_places=1, blank=True)
    start_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(
        default=UNAPPROVED, choices=PROJECT_STATUS)

    def __unicode__(self):
        return str(self.title)

    def save(self, **kwargs):
	    if not self.ordering:
	        ordering = Project.objects.all().aggregate(models.Max('ordering'))['ordering__max']
	        if ordering:
	            self.ordering = floor(ordering + 1)
	        else:
	            self.ordering = 1
	    super(Project, self).save(**kwargs)



class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='project_image')
    image = models.ImageField(upload_to='projects')
    ordering = models.DecimalField(default=1, max_digits=4, decimal_places=1, blank=True)

    def __unicode__(self):
        return str(self.project.title)

	def save(self, **kwargs):
	    if not self.ordering:
	        ordering = ProjectImage.objects.filter(project=self.project)\
	        .aggregate(models.Max('ordering'))['ordering__max']
	        if ordering:
	            self.ordering = floor(ordering + 1)
	        else:
	            self.ordering = 1
	    super(ProjectImage, self).save(**kwargs)


class Pledge(models.Model):
    user = models.ForeignKey(User, related_name='pledges')
    amount = IntegerRangeField(default=1000, min_value=1000)
    project = models.ForeignKey(Project, related_name='pledges')
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
