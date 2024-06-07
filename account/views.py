from django.shortcuts import render
from django.utils.translation import activate

def initial_content(request):
    # Ative o idioma espanhol
    activate('es')
    return render(request, 'account/account.html')
