# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('templates/<path:template_name>/', views.load_template, name='load_template'),
    path('api/check-authentication/', views.check_authentication, name='check_authentication'),
]
