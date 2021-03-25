from django.contrib import admin

from .models import Task, Project


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    model = Task

    list_display = ('title', 'pk', 'user', 'completed_on', 'created_on',)
    list_filter = ('user', 'completed_on',)

    search_fields = ('title','user',)
    ordering = ('user','created_on',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project

    list_display = ('title','parent','user','created_on')
    list_filter = ('user',)

    search_fields = ('title','user',)
    ordering = ('user','created_on',)