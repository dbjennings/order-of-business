from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from ..models import Task

class TaskIndexView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'oob/task_list.html'
    # Extra parameters
    inbox_view = False

    def get_queryset(self):
        '''Custom QuerySet based on passed keywords'''
        if self.inbox_view:
            return Task.objects.filter(user=self.request.user,
                                       project=None)
        else:
            return Task.objects.filter(user=self.request.user)


class TaskDetailView(DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'oob/task_detail.html'


class TaskCreateView(CreateView):
    model = Task
    fields = ('title','body','project',)
    template_name = 'oob/task_create.html'
    success_url = reverse_lazy('task-index')

    def form_valid(self, form):
        '''Sets the form user to the current user before saving'''
        # Set the form instance user field
        form.instance.user = self.request.user
        # Pass the updated form to CreateView.form_valid
        return super(TaskCreateView, self).form_valid(form)

class TaskUpdateView(UpdateView):
    model = Task
    fields = ('title','body','project','completed_on')
    template_name = 'oob/task_update.html'
    success_url = reverse_lazy('task-index')
    # Extra Parameters
    complete_toggle = False

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'oob/task_delete.html'
    success_url = reverse_lazy('task-index')