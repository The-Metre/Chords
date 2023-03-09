from django.urls import path
from intervals import views

urlpatterns = [
    path('<str:user_id>', views.index, name='user_practice'),
]