from django.shortcuts import render, render_to_response
from django.views.generic.base import View, TemplateView
from project.models import Project, Pledge, Message
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Sum
import datetime
from django.utils import timezone
from django.template import RequestContext
from django.core.urlresolvers import reverse
from project.forms import ProjectForm
import json, re
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


class ProjectListAPIView(View):
	def get(self, request, **kwargs):
		try:
			start = int(request.GET.get('start_index', ''))
			num_projects = int(request.GET.get('num_projects', ''))
			projects = Project.objects.all().order_by('ordering')[start:start + num_projects]
			data = []
			for p in projects:
				data.append(self.get_project_json_data(p, request))

			response = {'success': 'true', 'projects': data}
		except ValueError:
			response = {'success': 'false', 'projects': []}
		return HttpResponse(json.dumps(response))

	def get_project_json_data(self, p, request):
		image_urls = ['http://' + request.get_host() + url for url in p.get_image_urls()]
		data = {'id': p.id, 'title': p.title, 'summary': p.summary, 'description': p.description,
				'author_name': p.author.get_full_name(), 'goal': p.goal, 'days_remaining': p.days_remaining,
				'video_url': p.video_url, 'team': p.team, 'risks_and_challenges': p.risks_and_challenges,
				'percentage_pledged': p.percentage_pledged, 'pledged_amount': p.pledged_amount,
				'total_backers': p.total_backers, 'image_urls': image_urls,
				'primary_picture_url': p.primary_picture_url}
		return data

