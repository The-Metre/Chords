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
    song = Song.objects.get(id=song_id)
    error = None
    form = SongForm()
    if request.method == "POST":
        try:
            item = Sketch(text=request.POST['name'], song=song)
            item.full_clean()
            item.save()
            return redirect(song)
        except ValidationError:
            error = "You can't save an empty song item"

    return render(request, 'song_page.html', {'song': song, 'form': form, 'error': error})
