from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from pocket_chords.models import Song, Sketch
from pocket_chords.forms import SongForm

# Create your views here.

def home_page(request):
    return render(request, 'homepage.html', {'form': SongForm()})


def new_song(request):
    """ Create new song page """
    form = SongForm(data=request.POST)
    if form.is_valid():
        song = Song.objects.create(name=request.POST['name'])
        return redirect(song)
    else:
        return render(request, 'homepage.html', {"form": form})


def song_page(request, song_id):
    """ Show the user song page """
    song = Song.objects.get(pk=song_id)
    form = SongForm()
    if request.method == "POST":
        form = SongForm(data=request.POST)
        if form.is_valid():
            Sketch.objects.create(text=request.POST['name'], song=song)
            return redirect(song)
    return render(request, 'song_page.html', {'song': song, 'form': form})
