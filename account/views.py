from django.shortcuts import render
from django.utils.translation import activate

def initial_content(request):
    # Ative o idioma espanhol
    return render(request, 'account/account.html')
