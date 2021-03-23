from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Project(models.Model):
    title = models.CharField(max_length=100, blank=False)
    body = models.TextField(default='', blank=True)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True, editable=False)
    completed_on = models.DateTimeField(null=True, blank=True)


    def clean(self) -> None:
        '''Custom field validation prior to saving'''

        # Title must be non-empty
        if self.title=='':
            raise ValidationError('Projects title must have a non-empty value')
        # A project can't be its own parent
        if self.parent==self:
            raise ValidationError('Projects cannot be their own parent')
        # A project cannot be the child of a child (level max = 1)
        if self.parent and self.parent.parent: 
            raise ValidationError('Projects cannot be a sub-project of another sub-project')
        # A project cannot have both a parent and child (again, level max = 1)
        if self.parent and self.children.count()!=0:
            raise ValidationError('Projects cannot have both a parent and children')

        return super(Project, self).clean()

    def save(self, *args, **kwargs):
        '''Performs field validation before saving'''
        self.full_clean()
        return super(Project,self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title