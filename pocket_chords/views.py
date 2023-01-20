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
        error = "You can't have an empty song name field in Song model"
        return render(request, 'homepage.html', {"error": error})
    return redirect(f'/song_page/{new_song.id}/')


def song_page(request, song_id):
    """ Show the user song page """
    song = Song.objects.get(id=song_id)
    return render(request, 'song_page.html', {'song': song})

def add_item_to_song(request,song_id):
    song = Song.objects.get(pk=song_id)
    item = Sketch.objects.create(text=request.POST['chunk'], song=song)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        item.delete()
        error = "You can't save an empty song item"
        return render(request, 'song_page.html', {"error": error, "song": song})
    return redirect(f'/song_page/{song.id}/')