import json
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def singleGame(request):
    is_authenticated = request.user.is_authenticated 
    body = json.loads(request.body.decode('utf-8'))  # Decodifica e carrega o JSON diretamente

    context = {
        'playerOneName': body.get('playerOneName'),
        'playerTwoName': body.get('playerTwoName'),
        'skin': body.get('skin'),
        'is_authenticated': is_authenticated
    }

    return JsonResponse(context)