from django.http import JsonResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def load_template(request, template_name):
    return render(request, template_name)

def check_authentication(request):
    is_authenticated = request.user.is_authenticated
    print(is_authenticated)
    return JsonResponse({'is_authenticated': is_authenticated})
