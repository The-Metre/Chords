from django.urls import path
from intervals import views

urlpatterns = [
    path('<str:user_name>/', views.index, name='user_practice'),
]