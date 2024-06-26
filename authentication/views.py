import os
from urllib.parse import urlencode, urlparse, parse_qs
from django.contrib.auth import logout
from django.contrib.auth import login, authenticate  # , logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import translation
from django.views.decorators.csrf import ensure_csrf_cookie
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework_simplejwt.tokens import RefreshToken

from game.views import options
from .auth import IntraAuthenticationBackend
from .forms import CreateUserForm, LoginForm
from .services import exchange_code, generate_jwt_token


@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

@ensure_csrf_cookie
def initial_content(request):
    if request.headers.get('X-Requested-With') == 'Fetch':
        is_authenticated = request.user.is_authenticated

        if is_authenticated:
            return options(request)
        else:
            return login_view(request)
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


@ensure_csrf_cookie
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        response = redirect('authentication:login')
        response.delete_cookie("jwt_token")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
    else:
        return JsonResponse({"error": "User is not authenticated"}, status=401)

def register(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    form = CreateUserForm()
    if request.headers.get('X-Requested-With') == 'Fetch':
        context = {'form': form}
        return render(request, 'register.html', context)
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            device = TOTPDevice.objects.create(user=user, name='default')
            totp_url = device.config_url + '&' + urlencode({'issuer': 'ft_transcendence', 'label': user.email})
            parsed_url = urlparse(totp_url)
            query_params = parse_qs(parsed_url.query)
            context = {
                'secret': query_params.get('secret', [''])[0],
                'algorithm': query_params.get('algorithm', [''])[0],
                'issuer': query_params.get('issuer', [''])[0],
                'user': parsed_url.path.split('/')[-1],
                'totp_url': totp_url,
            }
            return render(request, 'otp_setup.html', context)
    return render(request, 'index.html')


def std_login_view(request):
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)

    form = LoginForm()
    language = request.headers.get('Content-Language', 'en')
    translation.activate(language)
    if request.headers.get('X-Requested-With') == 'Fetch':
        return render(request, 'std_login.html', {'form': form})
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'),
                                password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)
                response = redirect("authentication:initial_content")
                response.set_cookie("access_token", access_token, httponly=True)
                response.set_cookie("refresh_token", refresh_token, httponly=True)
                return response
        else:
            print(form.errors)
    return render(request, 'index.html')
