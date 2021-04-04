from django.forms import ModelForm, Form, CharField

from ..models import Project, Task

class TaskSearchForm(Form):
    '''Form for the task search bar'''
    query = CharField(max_length=100)

    query.widget.attrs.update({'placeholder': 'Search all tasks...',
                               'class': 'form-control',})

class TaskForm(ModelForm):

    class Meta:
        model = Task
        fields = ('title','body','project',)

    def __init__(self, *args, **kwargs):
        '''Uses the passed request to populate fields'''
        if kwargs['request']:
            self.request = kwargs.pop('request')
            super(TaskForm,self).__init__(*args, **kwargs)
            self.fields['project'].queryset = Project.objects.filter(user=self.request.user)
        else:
            super(TaskForm,self).__init__(*args, **kwargs)

