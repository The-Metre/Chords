import json

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.http.response import HttpResponse

from pocket_chords.models import Song, Sketch, ChordNotesRelation
from pocket_chords.forms import (
    SongForm, SketchForm, SongTextForm
    )

from accounts.models import User

import sys


def home_page(request):
    return render(request, 'homepage.html', {'form': SongForm()})


def new_song(request):
    """ Create new song page """
    form = SongForm(data=request.POST)
    if form.is_valid() and request.user.is_authenticated:
        song = Song()
        song.owner = request.user
        song.name = request.POST['name']
        song.save()
        return redirect(song)
    else:
        return render(request, 'homepage.html', {"form": form})

def song_page(request, song_id):
    song = Song.objects.get(pk=song_id)
    song_chunks = Sketch.objects.filter(song=song)
    form = SketchForm(request.POST or None)
    song_text_form = SongTextForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            chunk = form.save(commit=False)
            chunk.song = song
            chunk.save()
            return redirect('chunk_detail', chunk_id=chunk.id)
        else:
            return render(request, 'partials/chunk_form.html', {
                'form': form,
            })
        

    context = {
        'song': song,
        'form': form,
        'song_form': song_text_form,
        'song_chunks': song_chunks,
    }

    return render(request, 'song_page.html', context)


def create_chunk_form(request):
    context = {
        'form': SketchForm(),
    }
    return render(request, 'partials/chunk_form.html', context)

def chunk_detail(request, chunk_id):
    chunk = Sketch.objects.get(pk=chunk_id)
    context = {
        'chunk': chunk
    }
    return render(request, 'partials/chunk_detail.html', context)

def delete_chunk(request, chunk_id):
    chunk = Sketch.objects.get(pk=chunk_id)
    chunk.delete()
    return HttpResponse('')

def update_chunk(request, chunk_id):
    chunk = Sketch.objects.get(pk=chunk_id)
    form = SketchForm(request.POST or None, instance=chunk)
    
    if request.method == 'POST':
        if form.is_valid():
            chunk = form.save()
            return redirect('chunk_detail', chunk_id=chunk.id)
        
    context = {
        'form': form,
        'chunk': chunk,
    }

    return render(request, 'partials/chunk_form.html', context)


def create_song_text_form(request):
    context = {
        'song_form': SongTextForm(),
    }
    return render(request, 'partials/song_text_form.html', context)

def song_text_detail(request, song_id):
    song = Song.objects.get(pk=song_id)
    context = {
        'song': song
    }
    return render(request, 'partials/song_text_detail.html', context)

def update_song_text(request, song_id):
    song = Song.objects.get(pk=song_id)
    form = SongTextForm(request.POST or None, instance=song)
    
    print(form.is_valid())
    if request.method == 'POST':
        if form.is_valid():
            song = form.save()
            return redirect('song_text_detail', song_id=song.id)
        
    context = {
        'song_form': form,
        'song': song,
    }

    return render(request, 'partials/song_text_form.html', context)

def my_songs(request, user_email):
    owner = User.objects.get(email=user_email)
    return render(request, 'my_songs.html', {'owner': owner})