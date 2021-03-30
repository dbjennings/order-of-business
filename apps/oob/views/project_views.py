from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from apps.oob.models import Project
from apps.oob.forms import ProjectForm
from apps.oob.mixins import UserIsObjectUserMixIn


class ProjectIndexView(LoginRequiredMixin, ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'oob/project_index.html'

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)


class ProjectDetailView(LoginRequiredMixin, UserIsObjectUserMixIn, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'oob/project_detail.html'


class ProjectCreateView(LoginRequiredMixin, CreateView):
    form_class = ProjectForm
    template_name = 'oob/project_create.html'
    success_url = reverse_lazy('project-index')

    def get_form_kwargs(self):
        '''Appends the view request to the passed kwargs.
        Used to instatiate ProjectForm with current user data.'''
        kwargs = super(ProjectCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self,form):
        '''Sets the form user to the current user before saving'''
        # Set the form instance user field
        form.instance.user = self.request.user
        # Pass the updated form to CreateView.form_valid
        return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin, UserIsObjectUserMixIn, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'oob/project_update.html'
    success_url = reverse_lazy('project-index')

    def get_queryset(self):
        '''Manually populate the queryset with only current user data.'''
        return Project.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        '''Appends the view request to the passed kwargs.
        Used to instatiate ProjectForm with current user data.'''
        kwargs = super(ProjectUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs
    

class ProjectDeleteView(LoginRequiredMixin, UserIsObjectUserMixIn, DeleteView):
    model = Project
    template_name = 'oob/project_delete.html'
    success_url = reverse_lazy('project-index')

