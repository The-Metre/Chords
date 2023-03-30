from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse

from pocket_chords.models import Song, Sketch, ChordNotesRelation
from pocket_chords.forms import (
    SongForm, SketchForm, NewSongForm
    )

from accounts.models import User

import sys


def home_page(request):
    return render(request, 'homepage.html', {'form': SongForm(), 'songs_list': Song.objects.all()})


def new_song(request):
    """ Create new song page """
    form = SongForm(data=request.POST)
    if form.is_valid():
        song = Song()
        if request.user.is_authenticated:
            song.owner = request.user
        song.name = request.POST['name']
        song.save()
        return redirect(song)
    else:
        return render(request, 'homepage.html', {"form": form})

def new_song2(request):
    form = NewSongForm(data=request.POST)
    if form.is_valid():
        song = form.save(owner=request.user)
        return redirect(song)
    return render(request, 'homepage.html', {"form": form})

def song_page(request, song_id):
    """ Show the user song page """
    song = Song.objects.get(pk=song_id)
    form = SketchForm(initial={
        'text': "",
        'song': song
    })
    if request.method == "POST":
        form = SketchForm(request.POST)
        if form.is_valid():
            #Trying to save an element, if it alredy exists
            Sketch.objects.create(text=request.POST['text'], song=song)
            return redirect(song)
    return render(request, 'song_page.html', {'song': song, 'form': form})

def edit_chunk(request, chunk_id):
    print(chunk_id)
    return JsonResponse({"text": chunk_id}, status=200)

def my_songs(request, user_email):
    owner = User.objects.get(email=user_email)
    return render(request, 'my_songs.html', {'owner': owner})