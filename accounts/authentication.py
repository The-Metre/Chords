import sys
from accounts.models import ChordsUser, Token

class PasswordlessAuthenticationBackend(object):
    """ Serverside passwordless authentication process """

    def authenticate(self, uid):
        print('uid', uid, file=sys.stderr)
        if not Token.objects.filter(uid=uid).exists():
            print('no token found', file=sys.stderr)
            return None
        token = Token.objects.get(uid=uid)
        print('got token', file=sys.stderr)
        try:
            user = ChordsUser.objects.get(email=token.email)
            print('got user', file=sys.stderr)
            return user
        except ChordsUser.DoesNotExist:
            print('new user', file=sys.stderr)
            return ChordsUser.objects.create(email=token.email)
        
    def get_user(self, email):
        """ Get a user by email """
        return ChordsUser.object.get(email=email)