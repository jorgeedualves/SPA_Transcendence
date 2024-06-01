from django.shortcuts import render  # Importa a função render do módulo django.shortcuts
from django.views.decorators.csrf import ensure_csrf_cookie  # Importa o decorator ensure_csrf_cookie do módulo django.views.decorators.csrf

@ensure_csrf_cookie
def index(request):
    """
    View para a página inicial.
    
    Aplica o decorator ensure_csrf_cookie para garantir que o cookie CSRF seja enviado ao cliente.
    Renderiza o template 'index.html'.
    """
    return render(request, 'index.html')
