from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def account(request):
    if request.headers.get('X-Requested-With') == 'Fetch':
        return render(request, 'account.html')
    return render(request, 'index.html')