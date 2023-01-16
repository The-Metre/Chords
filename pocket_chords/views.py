from django.shortcuts import render, redirect
from pocket_chords.models import Song, Sketch

# Create your views here.

def home_page(request):

    return render(request, 'homepage.html')


def new_song(request):
    """ New song """
    if request.POST['song_name']:
        new_song = Song.objects.create(name=request.POST['song_name'], text='')
        return redirect(f'/song_page/{new_song.id}/')
    return redirect('/')


def song_page(request, song_id):
    """ Show the user song page """
    song = Song.objects.get(id=song_id)
    return render(request, 'song_page.html', {'song': song})

def add_item_to_song(request,song_id):
    song = Song.objects.get(pk=song_id)
    item = Sketch.objects.create(text=request.POST['chunk'], song=song)
    return redirect(f'/song_page/{song.id}/')