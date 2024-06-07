from django.contrib.auth.backends import BaseBackend
from authentication.models import CustomUser as User
from authentication.services import verify_jwt_token

class IntraAuthenticationBackend(BaseBackend):
    def authenticate(self, request, jwt_token=None, user_intra=None):
        if not isinstance(user_intra, dict):
            return None
        
        if jwt_token:
            user_data = verify_jwt_token(jwt_token)
            try:
                user = User.objects.get(username=user_data['id_42'])
            except User.DoesNotExist:
                user = User.objects.create_new_intra_user(user_intra)
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
