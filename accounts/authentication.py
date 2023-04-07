from accounts.models import Token, User
from django.contrib.auth.backends import ModelBackend

class PasswordlessAuthenticationBackend(ModelBackend):
    def authenticate(self, request, uid):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            username = token.email.split('@')[0]
            return User.objects.create(email=token.email, username=username)
        except Token.DoesNotExist:
            return None
    
    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        
    