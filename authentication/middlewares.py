from django.contrib.auth.middleware import get_user
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        jwt_auth = JWTAuthentication()
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if not access_token:
            # print('No access token')
            request.user = get_user(request)
            return

        try:
            validated_token = jwt_auth.get_validated_token(access_token)
            user = jwt_auth.get_user(validated_token)
            request.user = user
            # print('User authenticated')
        except InvalidToken:
            print('Invalid token')
            if not refresh_token:
                request.user = get_user(request)
                return
            try:
                # print('Refreshing token')
                refresh = RefreshToken(refresh_token)
                new_access_token = str(refresh.access_token)
                request.COOKIES['access_token'] = new_access_token
                validated_token = jwt_auth.get_validated_token(new_access_token.encode())
                user = jwt_auth.get_user(validated_token)
                request.user = user
            except TokenError:
                # print('Invalid refresh token')
                request.user = get_user(request)

    def process_response(self, request, response):
        if 'access_token' in request.COOKIES:
            print('Setting access token')
            response.set_cookie('access_token', request.COOKIES['access_token'], httponly=True)
        return response
