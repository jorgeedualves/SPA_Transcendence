from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from channels.db import database_sync_to_async
from urllib.parse import parse_qs
from .models import CustomUser as User
from .services import verify_jwt_token
from channels.auth import AuthMiddlewareStack
from channels.middleware import BaseMiddleware

@database_sync_to_async
def get_user(jwt_token):
    try:
        user_data = verify_jwt_token(jwt_token)
        return User.objects.get(username=user_data['id_42'])
    except User.DoesNotExist:
        return AnonymousUser()

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        params = parse_qs(query_string)
        jwt_token = params.get('token', [None])[0]

        if jwt_token:
            scope['user'] = await get_user(jwt_token)
        else:
            scope['user'] = AnonymousUser()

        close_old_connections()
        return await super().__call__(scope, receive, send)

def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))