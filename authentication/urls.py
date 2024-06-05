from django.urls import path  # Importa a função path do módulo django.urls
from core import views  # Importa o módulo views do diretório atual

# Lista de padrões de URL para o aplicativo
urlpatterns = [
    # Define a URL login/ que mapeia para a view 'login'
    path('', views.login, name='login'),
]
