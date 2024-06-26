from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Lista de padrões de URL para o aplicativo
urlpatterns = [
    path('', include('authentication.urls')),
	path('account/', include('account.urls')),
	path('game/', include('game.urls')),
]