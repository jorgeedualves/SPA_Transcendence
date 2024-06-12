from django.urls import path, include

# Lista de padrões de URL para o aplicativo
urlpatterns = [
    path('', include('authentication.urls')),
	path('account/', include('account.urls')),
	path('game/', include('game.urls')),
]
