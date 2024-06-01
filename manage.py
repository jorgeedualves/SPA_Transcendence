#!/usr/bin/env python
"""Utilitário de linha de comando do Django para tarefas administrativas."""
import os
import sys

def main():
    """Executa tarefas administrativas."""
    # Define a variável de ambiente 'DJANGO_SETTINGS_MODULE' com o valor 'core.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        # Importa a função execute_from_command_line do módulo django.core.management
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Lança uma exceção se o Django não puder ser importado, com uma mensagem de erro explicativa
        raise ImportError(
            "Não foi possível importar o Django. Você tem certeza de que ele está instalado e "
            "disponível na sua variável de ambiente PYTHONPATH? Você esqueceu de ativar um ambiente virtual?"
        ) from exc
    # Executa a função execute_from_command_line com os argumentos da linha de comando
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    # Chama a função main quando o script é executado diretamente
    main()
