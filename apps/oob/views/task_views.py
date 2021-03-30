from django.http.response import HttpResponseRedirect
from apps.oob.forms.task_forms import TaskForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q

from apps.oob.models import Task
from apps.oob.mixins import UserIsObjectUserMixIn


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
    form_class = TaskForm
    template_name = 'oob/task_create.html'
    success_url = reverse_lazy('task-index')

    def get_form_kwargs(self):
        kwargs = super(TaskCreateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        '''Sets the form user to the current user before saving'''
        # Set the form instance user field
        form.instance.user = self.request.user
        # Pass the updated form to CreateView.form_valid
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(LoginRequiredMixin,UserIsObjectUserMixIn, UpdateView):
    form_class = TaskForm
    template_name = 'oob/task_update.html'
    success_url = reverse_lazy('task-index')
    # Extra Parameters
    complete_toggle = False

    def get_queryset(self):
        '''Manually populate the queryset with only current user data.'''
        return Task.objects.filter(user=self.request.user)

    def get_form_kwargs(self):
        '''Appends the view request to the passed kwargs.
        Used to instatiate TaskForm with current user data.'''
        kwargs = super(TaskUpdateView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

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


class TaskDeleteView(LoginRequiredMixin, UserIsObjectUserMixIn, DeleteView):
    model = Task
    template_name = 'oob/task_delete.html'
    success_url = reverse_lazy('task-index')


class TaskSearchView(ListView):
    template_name = 'oob/search_results.html'
    
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            query_set = Task.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        return query_set