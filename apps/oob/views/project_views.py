from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy

from ..models import Project

class ProjectIndexView(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'oob/project_index.html'

class ProjectDetailView(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'oob/project_detail.html'

class ProjectCreateView(CreateView):
    model = Project
    fields = ('title','body','parent',)
    template_name = 'oob/project_create.html'
    success_url = reverse_lazy('project-index')

    def form_valid(self,form):
        '''Sets the form user to the current user before saving'''
        # Set the form instance user field
        form.instance.user = self.request.user
        # Pass the updated form to CreateView.form_valid
        return super().form_valid(form)

class ProjectUpdateView(UpdateView):
    model = Project
    fields = ('title','body','parent',)
    template_name = 'oob/project_update.html'
    success_url = reverse_lazy('project-index')

class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'oob/project_delete.html'
    success_url = reverse_lazy('project-index')

