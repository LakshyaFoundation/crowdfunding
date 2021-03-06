
from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from project.views import ProjectCreateView, ProjectDetailView, ProjectListView, ProjectListAPIView, \
    PledgeCreateAPIView

urlpatterns = patterns('',
                       url(r'^project/create/?$',
                           ProjectCreateView.as_view(), name='create project'),
                       url(r'^project/(?P<id>.*)/edit/?$',
                           ProjectCreateView.as_view(), name='edit project'),
                       url(r'^project/(?P<id>.*)/?$',
                           ProjectDetailView.as_view(), name='view project'),
                       url(r'^projects/?$', ProjectListView.as_view(),
                           name='view all projects'),
                       url(r'^_project/list/?$', ProjectListAPIView.as_view(), name='project-list-api'),
                       url(r'^_pledge/create/?$', csrf_exempt(PledgeCreateAPIView.as_view()), name='pledge-create-api'))
