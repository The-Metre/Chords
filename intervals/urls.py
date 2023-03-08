from django.urls import path
from intervals import views

urlpatterns = [
    path('', views.index, name='practice_index'),
]