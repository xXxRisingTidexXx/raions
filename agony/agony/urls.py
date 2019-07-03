from django.urls import path, include
from django.contrib.admin import site

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', site.urls)
]
