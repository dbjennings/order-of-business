from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    model = Task

    list_display = ('title', 'user', 'completed_on', 'created_on',)
    list_filter = ('user', 'completed_on',)

    search_fields = ('name','user',)
    ordering = ('user','created_on',)