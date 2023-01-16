from django.urls import path

from pocket_chords import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('song_page/<int:song_id>/', views.song_page, name='song_page'),
    path('song_page/new', views.new_song, name='new_song'),
    path('song_page/<int:song_id>/add_item', views.add_item_to_song, name='add_item_to_song'),
]