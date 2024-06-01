from django.urls import path  # Importa a função path do módulo django.urls
from . import views  # Importa o módulo views do diretório atual

# Lista de padrões de URL para o aplicativo
urlpatterns = [
    # Define a URL raiz (/) que mapeia para a view 'index'
    path('', views.index, name='index'),
]
