from django.conf.urls import url
from accounts import views

urlpatterns = [
    url('send_login_email', views.send_login_email, name='send_login_email'),
]