from django.urls import path
from intervals import views

urlpatterns = [
    path('fretboard', views.fretboard, name='fretboard'),
]