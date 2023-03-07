from django.core.management.base import BaseCommand
from pocket_chords.models import MusicNote, Chord, ChordNotesRelation
from project_tools.classes import GuitarStuffClass

class Command(BaseCommand):
    help = "Fills SQL tables (MusicNote, Chord, ChordNotesRelation) \
            with information"
    
    def handle(self, *args, **options):
        self.guitar = GuitarStuffClass()
        # Fill MusicNote table with all note names
        for note in self.guitar._notes:
            MusicNote.objects.get_or_create(name=note)

        # For each created note, create a related chord
        for note in MusicNote.objects.all():
            self._fill_the_chord_with_notes(note.name)

    def _fill_the_chord_with_notes(self, key_note):
        root = MusicNote.objects.get(name=key_note)
        scale_from_root = self.guitar.string_tuning(root.name)

        for chord_name in self.guitar._chord_formula:
            # Fill Chord sql table with chord name and related root note
            chord, _ = Chord.objects.get_or_create(name=f"{root.name} {chord_name}", root_note=root)
            notes = self.guitar._chord_formula[chord_name]
            for note in notes:
                # Fill Chord-Notes relationship table
                chord_note = MusicNote.objects.get(name=scale_from_root[note])
                ChordNotesRelation.objects.get_or_create(chord_name=chord, chord_note=chord_note)