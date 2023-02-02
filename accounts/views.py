import sys
import uuid
from django.shortcuts import render
from django.core.mail import send_mail

from accounts.models import Token

def send_login_email(request):
    """ send a link on login 
        through email
    """
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('saving uid', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_url(f'accounts/login?uid={uid}')
    send_mail(
        'Your login link for Pocket chords',
        f'Use this link to login:\n\n{url}',
        'noreply@pocket_chords',
        [email],
    )
    return render(request, 'login_email_sent.html')