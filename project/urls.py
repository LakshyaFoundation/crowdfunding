from django.conf.urls import patterns, url

from project.views import ProjectCreateView, ProjectListAPIView

urlpatterns = patterns('',
	url(r'^project/create/?$', ProjectCreateView.as_view(), name='create project'),
	url(r'^_project/list/?$', ProjectListAPIView.as_view(), name='project-list-api')
	)
