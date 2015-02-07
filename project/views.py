from django.shortcuts import render,render_to_response
from django.views.generic.base import View, TemplateView
from project.models import Project,Pledge,Message
from django.contrib import messages
from django.http import Http404,HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.db.models import Sum
import datetime
from django.utils import timezone
from django.template import RequestContext
from django.core.urlresolvers import reverse
from project.forms import ProjectForm
import json,re
# # Create your views here.
# def create_project(request):
# 	form = ProjectForm()
# 	return render(request,'project/create.html',{'form':form},context_instance=RequestContext(request))

class ProjectCreateView(TemplateView):
	template_name = 'project/create.html'
	def get_context_data(self, **kwargs):
	    context = TemplateView.get_context_data(self, **kwargs)
	    context['form'] = ProjectForm()
	    return context
	def post(self, request, *args, **kwargs):
		form_data = ProjectForm(request.POST)
		form_data.author = request.user
		if form_data.is_valid():
			form_data.save()
			response = {'success' :  'true'}
		# project = Project.objects().create(title=form_data.title,summary=form_data.summary,
		# 	description=form_data.description, author=request.user, goal=form_data.goal,
		# 	period=form_data.period,video_url=form_data.video_url,
		# 	risks_and_challenges=form_data.risks_and_challenges, ordering = 0, 
		# 	start_date=form_data.start_date, status=UNAPPROVED)
		else:
			response = {'success' : 'false'}
			
			print form_data.non_field_errors
			for field in form_data:
				print field.label
				print field.errors
		
		return HttpResponse(json.dumps(response))

class ProjectView(TemplateView):
	template_name = 'project/view.html'