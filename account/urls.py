from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('initial_content/', views.initial_content, name='initial_content'),
]
