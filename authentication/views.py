from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required
from .services import exchange_code, generate_jwt_token
from .auth import IntraAuthenticationBackend
import os
from django.utils import translation

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

@ensure_csrf_cookie
def initial_content(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    if request.headers.get('X-Requested-With') == 'Fetch':
        is_authenticated = request.user.is_authenticated
        template = 'account.html' if is_authenticated else 'login.html'
        return render(request, template)
    return render(request, 'index.html')

def login_view(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    if request.user.is_authenticated:
        return redirect('initial_content')

    auth_url = os.environ.get("AUTH_URL_INTRA")
    return render(request, 'login.html', {'auth_url': auth_url})

def intra_login(request):
    auth_url = os.environ.get("AUTH_URL_INTRA")
    return redirect(auth_url)

def intra_login_redirect(request):
    code = request.GET.get("code")
    try:
        user_intra = exchange_code(code)
        jwt_token = generate_jwt_token(user_intra)

        user = IntraAuthenticationBackend().authenticate(
            request=request,
            jwt_token=jwt_token,
            user_intra=user_intra
        )

        if user:
            login(request, user, "authentication.auth.IntraAuthenticationBackend")
            response = redirect("authentication:initial_content")
            response.set_cookie("jwt_token", jwt_token, httponly=True, samesite="Lax")
            return response
        else:
            return JsonResponse({"error": "Authentication failed"}, status=401)
    except Exception as e:
        print(f"Error during authentication: {e}")
        return JsonResponse({"error": "Authentication failed"}, status=401)

@login_required
def account(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    if request.headers.get('X-Requested-With') == 'Fetch':
        return render(request, 'account.html')
    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('jwt_token')
    response.delete_cookie('sessionid')
    request.session.flush()

    cookies_to_delete = ['_intra_42_session_production', '_mkra_stck', 'intra', 'locale', 'user.id']
    for cookie in cookies_to_delete:
        response.delete_cookie(cookie)

    return response
