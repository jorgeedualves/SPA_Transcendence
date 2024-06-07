from django.urls import path
from . import views

urlpatterns = [
    path('initial_content/', views.initial_content, name='initial_content'),
]
