from apps.oob.models import project
from django.forms import ModelForm, ModelChoiceField
from ..fields import ProjectChoiceIterator

from ..models import Project, Task


class TaskCreateForm(ModelForm):

    class Meta:
        model = Task
        fields = ('title','body','project',)

    def __init__(self, user, *args, **kwargs):
        super(TaskCreateForm,self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(user=user)

