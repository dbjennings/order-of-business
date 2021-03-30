from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from apps.oob.models import Task, Project
from apps.oob.forms import TaskSearchForm


class UserHomeView(TemplateView, ContextMixin):
    template_name = 'oob/user_home.html'

    def get_context_data(self, **kwargs):

        self.extra_context = {'tasks': Task.objects.filter(user=self.request.user),
                              'projects': Project.objects.filter(user=self.request.user),
                              'search_form': TaskSearchForm()}
        
        return super().get_context_data(**kwargs)
