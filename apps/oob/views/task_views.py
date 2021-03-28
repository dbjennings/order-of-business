from django.http.response import HttpResponseRedirect
from apps.oob.forms.task_forms import TaskCreateForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy

from ..models import Task
from ..mixins import UserIsObjectUserMixIn


class TaskIndexView(LoginRequiredMixin, ListView):
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


class TaskDetailView(LoginRequiredMixin, UserIsObjectUserMixIn, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'oob/task_detail.html'

    def test_func(self):
        object = self.get_object()
        return object.user == self.request.user


class TaskCreateView(LoginRequiredMixin, CreateView):
    form_class = TaskCreateForm
    template_name = 'oob/task_create.html'
    success_url = reverse_lazy('task-index')

    def get_form(self):
        '''Retrieves the form with the current user'''
        return self.form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        '''Sets the form user to the current user before saving'''
        # Set the form instance user field
        form.instance.user = self.request.user
        # Pass the updated form to CreateView.form_valid
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(UserIsObjectUserMixIn, UpdateView):
    model = Task
    fields = ('title','body','project','completed_on')
    template_name = 'oob/task_update.html'
    success_url = reverse_lazy('task-index')
    # Extra Parameters
    complete_toggle = False

    def post(self, request, *args, **kwargs):
        if self.complete_toggle:
            toggle_task = Task.objects.get(pk=self.kwargs['pk'])

            if toggle_task.is_complete:
                toggle_task.completed_on = None
            else:
                toggle_task.completed_on = timezone.now()
            
            toggle_task.save()
            return HttpResponseRedirect(self.success_url)
    
        return super().post(request, *args, **kwargs)


class TaskDeleteView(UserIsObjectUserMixIn, DeleteView):
    model = Task
    template_name = 'oob/task_delete.html'
    success_url = reverse_lazy('task-index')