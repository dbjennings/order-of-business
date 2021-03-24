from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from ..models import Task, Project

class UserHomeView(TemplateView, ContextMixin):
    template_name = 'oob/user_home.html'

    def get_context_data(self, **kwargs):

        self.extra_context = {'tasks': Task.objects.filter(user=self.request.user),
                              'projects': Project.objects.filter(user=self.request.user)}
        
        return super().get_context_data(**kwargs)