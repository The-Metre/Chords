import sys
from accounts.models import ChordsUser, Token

class PasswordlessAuthenticationBackend(object):
    """ Serverside passwordless authentication process """

    def authenticate(self, uid):
        print('uid', uid, file=sys.stderr)
        if not Token.objects.filter(uid=uid).exists():
            print('not toket found', file=sys.stderr)
            return None
        token = Token.objects.get(uid=uid)
        print('got a token', file=sys.stderr)
        try:
            user = ChordsUser.objects.get(email=token.email)
            print('got a user', file=sys.stderr)
            return user
        except ChordsUser.DoesNotExist:
            print('new_user', file=sys.stderr)
            return ChordsUser.objects.create(email=token.email)

    def get_user(self, email):
        return ChordsUser.objects.get(email=email)