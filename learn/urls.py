from django.conf.urls import url
from django.contrib.auth import views
from learn.views import *

urlpatterns = [
	url(r'^login/$', views.login, {'template_name': 'learn/auth/login.html'}),
	url(r'^logout/$', views.logout, {'next_page': '/login'}),
	url(r'^register/$', UserCreateView.as_view(), name="regsiter"),
    url(r'^$', ProjectListView.as_view(), name="project_list"),
    url(r'^project/(?P<pk>\d+)/$', ProjectDetailView.as_view(), name="project_detail"),
    url(r'^project/(?P<project_pk>\d+)/steps/$', StepListView.as_view(), name="step_list"),
]
