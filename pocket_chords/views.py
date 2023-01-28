from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib import messages

from pocket_chords.models import Song, Sketch
from pocket_chords.forms import SongForm, SketchForm

import sys
# Create your views here.

def home_page(request):
    return render(request, 'homepage.html', {'form': SongForm(), 'songs_list': Song.objects.all()})


def new_song(request):
    """ Create new song page """
    form = SongForm(data=request.POST)
    if form.is_valid():
        song = Song.objects.create(name=request.POST['name'])
        return redirect(song)
    else:
        return render(request, 'homepage.html',
                     {"form": form, 'songs_list': Song.objects.all()})


def song_page(request, song_id):
    """ Show the user song page """
    song = Song.objects.get(pk=song_id)
    form = SketchForm()
    if request.method == "POST":
        form = SketchForm(data=request.POST)
        if form.is_valid():
            # Trying to save an element, if it alredy exists
            try:
                Sketch.objects.create(text=request.POST['text'], song=song)
                return redirect(song)
            # if element already exist in a db
            except IntegrityError:
                # Show a message under a form
                messages.error(request, 'The chunk already exist. Please change your input and try again.')

    return render(request, 'song_page.html', {'song': song, 'form': form})
