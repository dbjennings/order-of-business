from apps.oob.forms.task_forms import TaskForm
from apps.oob.models import Project, Task
from apps.oob.forms import TaskSearchForm

def user_context(request):
    context = {}
    
    if request.user.is_authenticated:
        context = {
            'user_projects': Project.objects.filter(user=request.user).exclude(parent__isnull=False),
            'inbox_count': Task.objects.filter(user=request.user, project=None, completed_on=None).count(),
            'search_form': TaskSearchForm(),
            'task_form': TaskForm(request=request),
        }
    return context