from accounts.models import Token
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class PasswordlessAuthenticationBackend(ModelBackend):

    def authenticate(self, request, uid):
        User = get_user_model()
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None
    
    def get_user(self, email):
        User = get_user_model()
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
