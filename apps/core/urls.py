from django.urls import path
from django.urls.base import reverse_lazy
from django.urls.conf import include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from .views import CoreLoginView, CoreRegisterView

urlpatterns = [
    path('login', CoreLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page=reverse_lazy('landing')), name='logout'),
    path('register', CoreRegisterView.as_view(), name='register'),
]
