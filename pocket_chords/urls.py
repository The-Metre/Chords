from django.urls import path

from pocket_chords import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('songs_list/something_right_here/', views.song_list, name='song_list'),
    path('songs_list/new', views.new_song, name='new_song'),
]