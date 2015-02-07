from django.conf.urls import patterns, url

from project.views import ProjectCreateView

urlpatterns = patterns('',
	url(r'^project/create/?$', ProjectCreateView.as_view(),name='create project'))