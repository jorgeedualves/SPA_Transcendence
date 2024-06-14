from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import translation
from django.http import HttpResponse

@ensure_csrf_cookie
def account(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    if request.headers.get('X-Requested-With') == 'Fetch':
        return render(request, 'account.html')
    return render(request, 'index.html')

def initial_content(request):
    return HttpResponse("Initial Content")