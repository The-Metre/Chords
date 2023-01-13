from django.shortcuts import render, redirect
from pocket_chords.models import Song

# Create your views here.

def home_page(request):

    return render(request, 'homepage.html')


def new_song(request):
    """ New song """
    if request.POST['song_name']:
        Song.objects.create(name=request.POST['song_name'], text='')
    return redirect('/songs_list/something_right_here/')


def song_list(request):
    """ Show the user song list """  
    songs = Song.objects.all()
    return render(request, 'songs_list.html', {
        'songs' : songs
    })