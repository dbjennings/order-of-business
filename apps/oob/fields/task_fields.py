from django.db.models.query import QuerySet
from django.forms.models import ModelChoiceIterator, ModelChoiceField

import itertools
from collections import OrderedDict

class ProjectChoiceIterator(ModelChoiceIterator):

    def __iter__(self):
        if self.field.empty_label is not None:
            yield('', self.field.empty_label)

        for project in self.get_flattened_tree(self.queryset):
            yield self.choice(project)

    def get_flattened_tree(self, queryset: QuerySet):
        project_tree = OrderedDict()

        for project in queryset.select_related('parent'):

            if project.parent_id:
                project_tree.setdefault(project.parent_id, []).append(project)
            else:
                project_tree.setdefault(project.pk, []).append(project)
        
        flattened_tree = itertools.chain(*project_tree.itervalues())
        return flattened_tree

class ProjectChoiceField(ModelChoiceField):

    pass