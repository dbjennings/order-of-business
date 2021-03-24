from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

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

    def clean(self):
        '''Custom field validation'''
        # Title must be non-empty
        if self.title=='':
            raise ValidationError('Task titles must have a non-empty value')
        # Tasks can only be added to projects owned by the same user
        if self.project and self.user is not self.project.user:
                raise ValidationError('Tasks can only be added to projects owned by the same user')
        # Tasks can't be completed with a future date
        if self.completed_on and self.completed_on > timezone.now():
            raise ValueError('Tasks cannot be completed beyond timezone.now()')
        
        return super(Task, self).clean()

    def save(self, *args, **kwargs):
        '''Performs field validation before saving'''
        self.full_clean()
        
        return super(Task,self).save(*args, **kwargs)

    def complete_toggle_now(self):
        if self.completed_on:
            self.completed_on = None
        else:
            self.completed_on = timezone.now()

        return self.save()

    def __str__(self):
        return self.title