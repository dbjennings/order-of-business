from django.forms import ModelForm

from ..models import Project


class ProjectForm(ModelForm):

    class Meta:
        model = Project
        fields = ('title','body','parent',)

    def __init__(self, *args, **kwargs):
        '''Uses the passed request to choices for parent projects'''
        if kwargs['request']:
            self.request = kwargs.pop('request')
            super(ProjectForm,self).__init__(*args, **kwargs)

            # Only top-level projects can be choices
            query_set = Project.objects.filter(user=self.request.user, 
                                            parent=None)

            # Exclude self instance from choices on UpdateView
            if self.instance.pk is not None:
                query_set = query_set.exclude(pk=self.instance.pk)
                
            self.fields['parent'].queryset = query_set
        else:
            super(ProjectForm,self).__init__(*args, **kwargs)
