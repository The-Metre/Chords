from django.shortcuts import render
from pocket_chords.models import (
    ChordNotesRelation, Chord, MusicNote
)
# Create your views here.

def index(request, user_name=None):
    #song_chords = ['F major', 'B minor']
    song_chords = Chord.objects.all()
    relations = {chord: ' '.join([note.chord_note.name for note in
                    ChordNotesRelation.objects.filter(
                        chord_name=Chord.objects.get(name=chord))
                        ]) for chord in song_chords
                }
                
    return render(request, 'fretboard.html', {'chords': relations.items(),'chord_select': relations.items(), 'user_name': user_name})