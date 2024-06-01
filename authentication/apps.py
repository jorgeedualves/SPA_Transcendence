from django.apps import AppConfig  # Importa a classe base AppConfig do módulo django.apps


class AuthenticationConfig(AppConfig):
    """
    Configuração da aplicação 'authentication'.
    
    Esta classe configura a aplicação Django chamada 'authentication'.
    """
    # Define o tipo padrão de campo auto-incremental para modelos nesta aplicação
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nome da aplicação. Este nome é usado pelo Django para identificar a aplicação.
    name = 'authentication'
