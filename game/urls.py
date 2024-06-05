from django.urls import path  # Importa a função path do módulo django.urls
from core import views  # Importa o módulo views do core

# Lista de padrões de URL para o aplicativo
urlpatterns = [
    path('options/', views.options, name='options'),
	path('singleGame/', views.singleGame, name='singleGame'),
	path('pong/', views.pong, name='pong'),
]
