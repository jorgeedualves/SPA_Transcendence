"""
Configurações do Django para o projeto core.

Gerado por 'django-admin startproject' usando Django 4.2.11.

Para mais informações sobre este arquivo, veja
https://docs.djangoproject.com/en/4.2/topics/settings/

Para a lista completa de configurações e seus valores, veja
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Construindo caminhos dentro do projeto como: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações de desenvolvimento rápido - inadequadas para produção
# Veja https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# AVISO DE SEGURANÇA: mantenha a chave secreta usada em produção em segredo!
SECRET_KEY = 'django-insecure-abyqy2^-=wja(v8it%7u)47b!(go7g7+_1odx*7lmz=-7yb#=8'

# AVISO DE SEGURANÇA: não execute com o debug ativado em produção!
DEBUG = True

ALLOWED_HOSTS = []  # Lista de hosts/nomes de domínio permitidos

# Definição da aplicação

INSTALLED_APPS = [
    # Aplicações Django incluídas por padrão
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'game',
    'account'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Diretórios de templates
        'APP_DIRS': True,  # Habilita carregamento de templates de diretórios de apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Configuração do banco de dados
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Caminho para o banco de dados SQLite
    }
}

# Validação de senha
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internacionalização
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'  # Código de idioma

# Diretório para os arquivos de tradução
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGES = [
    ('en', 'English'),
    ('es', 'Español'),
    ('pt-br', 'Portuguese (Brazil)'),
    ('fr', 'French'),
    # Adicione mais idiomas conforme necessário
]

TIME_ZONE = 'UTC'  # Fuso horário

USE_I18N = True  # Habilita tradução

USE_TZ = True  # Habilita suporte a timezone

# Arquivos estáticos (CSS, JavaScript, Imagens)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Diretórios de arquivos estáticos
STATIC_URL = 'static/'  # URL para servir arquivos estáticos

# Tipo de campo de chave primária padrão
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
