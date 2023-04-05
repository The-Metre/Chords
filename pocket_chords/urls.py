from django.urls import path

from pocket_chords import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('song_page/<int:song_id>/', views.song_page, name='song_page'),
    path('song_page/new', views.new_song, name='new_song'),
    path('songs/users/<str:user_email>', views.my_songs, name='my_songs'),

    path('htmx/chunk_form/', views.create_chunk_form, name='chunk_form'),

    # Api route
    path('song_page/chunk/<int:chunk_id>', views.chunk_detail, name='chunk_detail'),
]

