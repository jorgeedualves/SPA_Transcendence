from django.http import JsonResponse  # Importa JsonResponse para retornar respostas JSON
from django.shortcuts import render  # Importa render para renderizar templates HTML

def index(request):
    """
    View para a página inicial.
    Renderiza o template 'index.html'.
    """
    return render(request, 'index.html')

def load_template(request, template_name):
    """
    View para carregar e renderizar um template específico.
    O nome do template é passado como argumento na URL.
    """
    return render(request, template_name)

def check_authentication(request):
    """
    View para verificar se o usuário está autenticado.
    Retorna uma resposta JSON indicando o status de autenticação do usuário.
    """
    is_authenticated = request.user.is_authenticated  # Verifica se o usuário está autenticado
    print(is_authenticated)  # Imprime o status de autenticação no console
    return JsonResponse({'is_authenticated': is_authenticated})  # Retorna o status como resposta JSON
