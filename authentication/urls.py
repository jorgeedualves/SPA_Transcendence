from django.urls import path

from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.index, name='index'),
    path('initial_content/', views.initial_content, name='initial_content'),
    path('login/', views.login_view, name='login'),
    # path('logout/', views.logout_view, name='logout'),
    path('oauth2/login/', views.intra_login, name='intra_login'),
    path('oauth2/login/redirect/', views.intra_login_redirect, name='intra_login_redirect'),
    path('register/', views.register, name='register'),
    path('std_login/', views.std_login_view, name='std_login'),
]
