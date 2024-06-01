"""
Configuração ASGI para o projeto core.

Este arquivo expõe o callable ASGI como uma variável de nível de módulo chamada ``application``.

Para mais informações sobre este arquivo, veja
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Define a variável de ambiente 'DJANGO_SETTINGS_MODULE' com o valor 'core.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Obtém a aplicação ASGI configurada, que será usada pelo servidor ASGI para lidar com requisições
application = get_asgi_application()
