"""
Configurações do Django para o projeto core.

Gerado por 'django-admin startproject' usando Django 4.2.11.

Para mais informações sobre este arquivo, veja
https://docs.djangoproject.com/en/4.2/topics/settings/

Para a lista completa de configurações e seus valores, veja
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
from dotenv import load_dotenv

# Construindo caminhos dentro do projeto como: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = os.environ.get('REDIRECT_URI')
AUTH_URL_INTRA = os.environ.get('AUTH_URL_INTRA')

# Verifique se todas as variáveis estão definidas
if not all([SECRET_KEY, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, AUTH_URL_INTRA]):
    raise ValueError("One or more environment variables are not set.")


DEBUG = True

ALLOWED_HOSTS = ['*']

# Definição da aplicação

INSTALLED_APPS = [
    # Aplicações Django incluídas por padrão
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'rest_framework',
    'rest_framework_simplejwt',
    'authentication',
    'game',
    'account'
]

ASGI_APPLICATION = 'core.asgi.application'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
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
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DB'),
#         'USER': os.getenv('POSTGRES_USER'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#         'HOST': os.getenv('POSTGRES_HOST'),
#         'PORT': os.getenv('POSTGRES_PORT'),
#     }
# }

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

AUTH_USER_MODEL = 'authentication.CustomUser'

LOGIN_URL = 'authentication:login'
LOGIN_REDIRECT_URL = 'authentication:account'
LOGOUT_REDIRECT_URL = 'authentication:login'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'authentication.auth.IntraAuthenticationBackend',  # Adjust this if needed
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'ALGORITHM': 'HS256',
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
}