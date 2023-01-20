from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from pocket_chords.models import Song, Sketch

# Create your views here.

def home_page(request):

    return render(request, 'homepage.html')


def new_song(request):
    """ Create new song page """
    new_song = Song(name=request.POST['song_name'])
    try:
        new_song.full_clean()
        new_song.save()
    except ValidationError:
        error = "You can't save an empty song item"
        return render(request, 'homepage.html', {"error": error})
    return redirect(f'/song_page/{new_song.id}/')


def song_page(request, song_id):
    """ Show the user song page """
    song = Song.objects.get(id=song_id)
    error = None
    if request.method == "POST":
        try:
            item = Sketch(text=request.POST['chunk'], song=song)
            item.full_clean()
            item.save()
            return redirect(f'/song_page/{song.id}/')
        except ValidationError:
            error = "You can't save an empty song item"

    return render(request, 'song_page.html', {'song': song, 'error': error})
