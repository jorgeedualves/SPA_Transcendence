from django.http import JsonResponse
import json
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

@ensure_csrf_cookie
def initial_content(request):
    is_authenticated = request.user.is_authenticated
    is_authenticated = True
    template = 'account.html' if is_authenticated else 'login.html'
    return render(request, template)

@ensure_csrf_cookie
def options(request):
    if request.headers.get('X-Requested-With') == 'Fetch':
        return render(request, 'options.html')
    return render(request, 'index.html')

@ensure_csrf_cookie
def singleGame(request):
    is_authenticated = request.user.is_authenticated
    if request.headers.get('X-Requested-With') == 'Fetch':
        body = json.loads(request.body.decode('utf-8'))  # Decode and load the JSON directly

        context = {
            'playerOneName': body.get('playerOneName'),
            'playerTwoName': body.get('playerTwoName'),
            'skin': body.get('skin'),
            'is_authenticated': is_authenticated
        }

        return JsonResponse(context)
    return render(request, 'index.html')

@ensure_csrf_cookie
def login(request):
    if request.headers.get('X-Requested-With') == 'Fetch':
        return render(request, 'login.html')
    return render(request, 'index.html')

@ensure_csrf_cookie
def account(request):
    if request.headers.get('X-Requested-With') == 'Fetch':
        return render(request, 'account.html')
    return render(request, 'index.html')

@ensure_csrf_cookie
def pong(request):
	if request.headers.get('X-Requested-With') == 'Fetch':
		return render(request, 'pong.html')
	return render(request, 'index.html')