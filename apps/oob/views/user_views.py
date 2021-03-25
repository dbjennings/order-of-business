from django.views.generic import TemplateView, FormView
from django.views.generic.base import ContextMixin
from django.db.models import Q
from django.views.generic.list import ListView

from ..models import Task, Project
from ..forms import UserSearchForm

class UserHomeView(TemplateView, ContextMixin):
    template_name = 'oob/user_home.html'

    def get_context_data(self, **kwargs):

        self.extra_context = {'tasks': Task.objects.filter(user=self.request.user),
                              'projects': Project.objects.filter(user=self.request.user),
                              'search_form': UserSearchForm()}
        
        return super().get_context_data(**kwargs)

class UserSearchView(ListView):
    template_name = 'oob/search_results.html'
    
    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            query_set = Task.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))
        return query_set