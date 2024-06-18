#game/views.py
from django.shortcuts import render
from django.utils import translation
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
import json

@ensure_csrf_cookie
def options(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    if request.headers.get('X-Requested-With') == 'Fetch':
        context = {'username': request.user.username}
        return render(request, 'options.html', context)
    return render(request, 'index.html')

@ensure_csrf_cookie
def pong(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    if request.headers.get('X-Requested-With') == 'Fetch':
        is_authenticated = request.user.is_authenticated
        body = json.loads(request.body.decode('utf-8'))
        context = {
            'playerOneName': body.get('playerOneName'),
            'playerTwoName': body.get('playerTwoName'),
            'skin': body.get('skin'),
            'is_authenticated': is_authenticated
        }
        return render(request, 'pong.html', context)
    return render(request, 'index.html')

@login_required
def tournament(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    if request.headers.get('X-Requested-With') == 'Fetch':
        return render(request, 'tournament.html')
    return render(request, 'index.html')

@login_required
def get_current_user(request):
    user = request.user
    return JsonResponse({'id': user.id})