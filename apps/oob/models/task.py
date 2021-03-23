from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from .project import Project

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100, blank=False)
    body = models.TextField(max_length=500, default='', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='tasks', null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    modified_on = models.DateTimeField(auto_now=True, editable=False)
    completed_on = models.DateTimeField(null=True, blank=True)

    def clean(self) -> None:
        '''Custom field validation'''
        
        # Title must be non-empty
        if self.title=='':
            raise ValidationError('Projects must have a non-empty value')
        
        return super(Task, self).clean()

    def save(self, *args, **kwargs):
        '''Performs field validation before saving'''
        self.full_clean()
        
        return super(Task,self).save(*args, **kwargs)

    def __str__(self):
        return self.title