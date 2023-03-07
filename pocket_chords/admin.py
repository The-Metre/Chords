from django.contrib import admin
from pocket_chords.models import (
    Song, Sketch, MusicNote, Chord, \
    ChordNotesRelation
)
# Register your models here.

admin.site.register(Song)
admin.site.register(Sketch)
admin.site.register(MusicNote)
admin.site.register(ChordNotesRelation)
admin.site.register(Chord)