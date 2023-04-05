import json

from django.views.decorators.csrf import csrf_exempt
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

""" def new_song2(request):
    form = NewSongForm(data=request.POST)
    if form.is_valid():
        song = form.save(owner=request.user)
        return redirect(song)
    return render(request, 'homepage.html', {"form": form}) """

def song_page1(request, song_id):
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

def song_page(request, song_id):
    song = Song.objects.get(pk=song_id)
    form = SketchForm(initial={
        'text': "",
        'song': song,
    })

    if request.method == 'POST':
        form = SketchForm(request.POST)
        if form.is_valid():
            chunk = Sketch.objects.create(text=request.POST['text'], song=song)
            return redirect('chunk_detail', pk=chunk.id)
    
    return render(request, 'song_page.html', {'song': song, 'form': form})


def create_chunk_form(request):
    context = {
        'form': SketchForm(),
    }
    return render(request, 'partials/chunk_form.html', context)

def chunk_detail(request, chunk_id):
    chunk = Sketch.objects.get(song=chunk_id)
    context = {
        'chunk': chunk
    }
    return render(request, 'song_page.html', context)


def my_songs(request, user_email):
    owner = User.objects.get(email=user_email)
    return render(request, 'my_songs.html', {'owner': owner})