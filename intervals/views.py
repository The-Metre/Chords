from django.shortcuts import render
import json

from pocket_chords.models import (
    ChordNotesRelation, Chord, MusicNote
)
# Create your views here.

def index(request, user_name=None):
    song_chords = Chord.objects.all()
    relations = {chord.name: ' '.join([note.chord_note.name for note in
                    ChordNotesRelation.objects.filter(
                        chord_name=Chord.objects.get(name=chord))
                        ]) for chord in song_chords
                }

    """ a = json.dumps(relations)
    print(a)
    for item in relations.items():
        print(item) """

    return render(request, 'fretboard.html', {'stuff':relations, 'chords': relations.items(),'chord_select': relations.items(), 'user_name': user_name})