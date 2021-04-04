from apps.oob.models import Project, Task
from apps.oob.forms import TaskSearchForm

def user_context(request):
    context = {}
    
    if request.user.is_authenticated:
        context = {
            'user_projects': Project.objects.filter(user=request.user).exclude(parent__isnull=False),
            'inbox_count': Task.objects.filter(user=request.user, project=None, completed_on=None).count(),
            'search_form': TaskSearchForm()
        }
    print(context)
    return context