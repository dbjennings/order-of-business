from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic import TemplateView

from apps.core.views import CoreLandingView

urlpatterns = [
    path('', CoreLandingView.as_view(), name='landing'),
    path('admin/', admin.site.urls),
    path('user/', include('apps.core.urls')),
    path('oob/', include('apps.oob.urls')),
]
