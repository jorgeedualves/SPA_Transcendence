from django.urls import path  # Importa a função path do módulo django.urls
from core import views  # Importa o módulo views do core

# Lista de padrões de URL para o aplicativo
urlpatterns = [
    path('options/', views.options, name='options'),
	path('pong/', views.pong, name='pong'),
	path('tournament/', views.tournament, name='tournament'),
]
