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

class ProjectCreateView(TemplateView):

    template_name = 'project/create.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        project = Project.objects.get(id=kwargs.get('id'))
        if project and self.request.user == project.author:
            context['form'] = ProjectForm(instance=project)
            context['mode'] = 'edit'
            context['id'] = project.id
        elif not project:
            context['form'] = ProjectForm()
            context['mode'] = 'create'
        else:
            raise Http404
        return context

    def post(self, request, *args, **kwargs):
        project = Project(author=request.user)
        id = kwargs.get('id')
        if id:
            project = Project.objects.get(id=id)
        form_data = ProjectForm(request.POST, instance=project)
        if form_data.is_valid():
            form_data.save()
            response = {'success':  'true'}
        else:
            response = {'success': 'false'}
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


class ProjectDetailView(TemplateView):
    template_name = 'project/detail.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        project = Project.objects.get(id=kwargs.get('id'))
        context['project'] = project
        return context


class ProjectListView(TemplateView):
    template_name = 'project/list.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        # project = Project.objects.get(id=kwargs.get('id'))
        context['projects'] = Project.objects.all()
        return context
