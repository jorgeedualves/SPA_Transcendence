"""
Configuração WSGI para o projeto core.

Este arquivo expõe o callable WSGI como uma variável de nível de módulo chamada ``application``.

Para mais informações sobre este arquivo, veja
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application  # Importa a função get_wsgi_application do módulo django.core.wsgi

# Define a variável de ambiente 'DJANGO_SETTINGS_MODULE' com o valor 'core.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Obtém a aplicação WSGI configurada
application = get_wsgi_application()
