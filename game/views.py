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

def pong(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    
    if request.headers.get('X-Requested-With') == 'Fetch':
        try:
            body = request.body.decode('utf-8')
            if not body:
                return JsonResponse({"error": "Empty request body"}, status=400)
            data = json.loads(body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        context = {
            'playerOneName': data.get('playerOneName'),
            'playerTwoName': data.get('playerTwoName'),
            'skin': data.get('skin'),
            'is_authenticated': request.user.is_authenticated
        }
        return render(request, 'pong.html', context)
    
    return render(request, 'index.html')

@login_required
def tournament(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    
    if request.headers.get('X-Requested-With') == 'Fetch':
        try:
            body = request.body.decode('utf-8')
            if not body:
                return JsonResponse({"error": "Empty request body"}, status=400)
            data = json.loads(body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        context = {
            'playerOneName': data.get('playerOneName'),
            'playerTwoName': data.get('playerTwoName'),
            'skin': data.get('skin'),
        }
        return render(request, 'tournament.html', context)
    
    return render(request, 'index.html')

@login_required
def get_current_user(request):
    user = request.user
    return JsonResponse({'id': user.id})