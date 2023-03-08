from django.shortcuts import render
from pocket_chords.models import (
    ChordNotesRelation, Chord, MusicNote
)
# Create your views here.

def fretboard(request):
    song_chords = ['F m7', 'B minor', 'A minor', 'D 7', 'A major', 'G m7', 'F minor']
    relations = dict()
    for smth in song_chords:
        chord = ChordNotesRelation.objects.filter(chord_name=Chord.objects.get(name=smth))
        for item in chord:
            if item.chord_name.name not in relations:
                relations[item.chord_name.name] = item.chord_note.name
            else:
                relations[item.chord_name.name] += f' {item.chord_note.name}'
    print(relations)
    return render(request, 'fretboard.html', {'chords':relations.items()})