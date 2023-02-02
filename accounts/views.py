import sys
import uuid

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from accounts.models import Token

def login(request):
    """ registraion in a system """
    print('login.view', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)
    return redirect('/')

def send_login_email(request):
    """ send a link on login 
        through email
    """
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email, uid=uid)
    print('saving uid', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(f'accounts/login?uid={uid}')
    send_mail(
        'Your login link for Pocket chords',
        f'Use this link to login:\n\n{url}',
        'noreply@pocket_chords',
        [email],
    )
    return render(request, 'login_email_sent.html')

def logout(request):
    auth_logout(request)
    return redirect('/')