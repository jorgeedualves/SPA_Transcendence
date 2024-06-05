from django.urls import path, include
from . import views  # Importa as views do módulo atual

# Lista de padrões de URL para o aplicativo
urlpatterns = [
    path('', views.index, name='index'),
	path('initial_content/', views.initial_content, name='initial_content'),
	path('authentication/', include('authentication.urls')),
	path('account/', include('account.urls')),
	path('game/', include('game.urls')),
]
