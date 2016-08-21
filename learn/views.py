from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, CreateView
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django import forms
from learn.models import Project, Step, Progress
# from learn.forms import UserForm

from braces.views import LoginRequiredMixin


class UserCreateView(CreateView):
	model = User 
	template_name = "learn/auth/register.html"
	fields = ["username", "email", "password"]
	success_url = "/login"

	def form_valid(self, form):
		user = User.objects.create_user(
			username=form.cleaned_data["username"],
			email=form.cleaned_data["email"],
			password=form.cleaned_data["password"]
		)

		return redirect(self.get_success_url())

	def get_form(self, form_class=None):
		form = super(UserCreateView, self).get_form(form_class)
		form.fields["password"].widget = forms.PasswordInput()
		return form

class ProjectListView(ListView):
	model = Project 
	template_name = "learn/project/list.html"

class ProjectDetailView(DetailView):
	model = Project 
	template_name = "learn/project/detail.html"

	def get_context_data(self, **kwargs):
		context = super(ProjectDetailView, self).get_context_data(**kwargs)

		context["steps"] = self.object.get_steps()

		context["progress"] = Progress.objects.filter(user=self.request.user, project=self.object).first()
		context["max_step"] = max([s.order for s in context["steps"]])

		if context["progress"] and context["max_step"] > 0:
			context["total_progress"] = (context["progress"].step / context["max_step"]) * 100
		return context 

class StepListView(LoginRequiredMixin, ListView):
	login_url = "/admin/"
	model = Step 
	paginate_by = 1
	template_name = "learn/step/list.html"

	def get_queryset(self):
		queryset = super(StepListView, self).get_queryset().filter(project__id=self.kwargs["project_pk"]).order_by("order")		
		return queryset

	def get_context_data(self, **kwargs):
		context = super(StepListView, self).get_context_data(**kwargs)
		context["steps"] = self.get_queryset()

		if "page" in self.request.GET:
			step = get_object_or_404(Step, pk=int(self.request.GET['page']))
		else:
			step = context["steps"].first()

		progress, created = Progress.objects.get_or_create(user=self.request.user, project=step.project)
		if progress.step < step.order:
			progress.step = step.order 
			progress.save()
		
		return context
