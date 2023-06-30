from django.urls import path

from pocket_chords import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('song_page/<int:song_id>/', views.song_page, name='song_page'),
    path('song_page/new', views.new_song, name='new_song'),
    path('songs/users/<str:user_email>', views.my_songs, name='my_songs'),

    # HTMX routes
    # For song chunks
    path('htmx/chunk_form/', views.create_chunk_form, name='chunk_form'),
    path('htmx/chunk_detail/<int:chunk_id>/', views.chunk_detail, name='chunk_detail'),
    path('htmx/chunk_detail/<int:chunk_id>/delete/', views.delete_chunk, name='delete_chunk'),
    path('htmx/chunk_detail/<int:chunk_id>/update/', views.update_chunk, name='update_chunk'),
    # For song text
    path('htmx/song_detail/<int:song_id>/', views.song_text_detail, name='song_text_detail'),
    path('htmx/song_detail/<int:song_id>/update/', views.update_song_text, name='update_song_text'),
    path('htmx/song_text_form/', views.create_song_text_form, name='song_text_form'),

]

