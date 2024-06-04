from django.urls import path
from . import views  # Importa as views do módulo atual
from game import views as game_views

# Lista de padrões de URL para o aplicativo
urlpatterns = [
    # Define a URL raiz (/) que mapeia para a view 'index'
    path('', views.index, name='index'),
    
    # Define a URL para carregar templates dinâmicos, mapeada para a view 'load_template'
    # <path:template_name> captura o nome do template a ser carregado
    path('templates/<path:template_name>/', views.load_template, name='load_template'),
    
    # Define a URL para a API de verificação de autenticação, mapeada para a view 'check_authentication'
    path('api/check-authentication/', views.check_authentication, name='check_authentication'),

	path('singleGame/', game_views.singleGame, name='singleGame'),
]
