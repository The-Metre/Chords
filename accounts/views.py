from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages


def send_login_email(request):
    """ send a link on login 
        through email
    """
    email = request.POST['email']
    send_mail(
        'Your login link for Chords',
        'body text',
        'noreply@chords',
        [email],
    )
    messages.success(
        request,
        'Check your email, we sent you a link, \
        which you can use to login into the site'
    )
    return redirect('/')