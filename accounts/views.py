from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import auth, messages

from accounts.models import Token

import sys

def send_login_email(request):
    """ send a link on login 
        through email
    """
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Chords',
        message_body,
        'noreply@chords',
        [email],
    )
    messages.success(
        request,
        'Check your email, we sent you a link, \
        which you can use to login into the site'
    )
    return redirect('/')

def login(request):
    """ Register log in system """
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')