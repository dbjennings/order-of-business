from django.urls import path
from django.urls.conf import include
from django.views.generic.base import TemplateView

from apps.oob.views import TaskIndexView, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskSearchView
from apps.oob.views import ProjectUpdateView, ProjectCreateView, ProjectDetailView, ProjectIndexView, ProjectDeleteView


urlpatterns = [
    path('', TemplateView.as_view(template_name='oob/user_home.html'), name='user-home'),
    path('search/', TaskSearchView.as_view(), name='search'),
    path('task/', include([
        path('', TaskIndexView.as_view(), name='task-index'),
        path('inbox', TaskIndexView.as_view(inbox_view=True), name='inbox'),
        path('create', TaskCreateView.as_view(), name='task-create'),
        path('<int:pk>/', include([
            path('', TaskDetailView.as_view(), name='task-detail'),
            path('update', TaskUpdateView.as_view(), name='task-update'),
            path('complete', TaskUpdateView.as_view(complete_toggle=True), name='task-complete'),
            path('delete', TaskDeleteView.as_view(), name='task-delete'),
        ]))
    ])),
    path('project/', include([
        path('', ProjectIndexView.as_view(), name='project-index'),
        path('create', ProjectCreateView.as_view(), name='project-create'),
        path('<int:pk>/', include([
            path('', ProjectDetailView.as_view(), name='project-detail'),
            path('update', ProjectUpdateView.as_view(), name='project-update'),
            path('delete', ProjectDeleteView.as_view(), name='project-delete'),
        ]))
    ]))
]
