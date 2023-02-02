from django.urls import path
from accounts import views

urlpatterns = [
    path(r'^send_email$', views.send_login_email, name='send_login_email'),
    path(r'^login', views.login, name='login'),
    path(r'^logout', views.logout, name='logout'),
]

