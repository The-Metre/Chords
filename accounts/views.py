from django.shortcuts import render, redirect
from django.core.mail import send_mail

#from accounts.models import Token

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
    return redirect('/')