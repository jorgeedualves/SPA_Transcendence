from django.urls import path  # Importa a função path do módulo django.urls
from . import views  # Importa o módulo views do diretório atual

app_name = 'authentication'

urlpatterns = [
    path('', views.index, name='index'),
    path('initial_content/', views.initial_content, name='initial_content'),
    path('login/', views.login_view, name='login'),
    path('account/', views.account, name='account'),
    path('logout/', views.logout_view, name='logout'),
    path('oauth2/login/', views.intra_login, name='intra_login'),
    path('oauth2/login/redirect/', views.intra_login_redirect, name='intra_login_redirect'),
]