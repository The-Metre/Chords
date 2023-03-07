from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from pocket_chords.models import (
    Song, Sketch, Chord, MusicNote, ChordNotesRelation
    )
from project_tools.classes import GuitarStuffClass

MUSIC_NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
User = get_user_model()

class SongModelTest(TestCase):
    ''' test Song model '''

    def test_get_absolute_url(self):
        """ Test: handeled absolute url"""
        song = Song.objects.create(name="test song")
        self.assertEqual(song.get_absolute_url(), f'/song_page/{song.id}/')


    def test_cannot_save_empty_name_song(self):

        song = Song(name="")
        with self.assertRaises(ValidationError):
            song.full_clean()
            song.save

    def test_duplicate_items_are_invalid_in_song_model(self):
        """ test: cannot save duplicate items in Song model """
        Song.objects.create(name="Test item")
        with self.assertRaises(ValidationError):
            new_song = Song(name="Test item")
            new_song.full_clean()

    def test_song_can_have_owner(self):
        user = User.objects.create(email='a@b.com')
        song = Song.objects.create(owner = user, name='test name')
        self.assertIn(song, user.song_set.all())

    def test_song_owner_is_optional(self):
        Song.objects.create(name='test name')


class SketchModelTest(TestCase):
    ''' test Sketch model '''

    def test_default_text(self):
        """ test model field """
        item = Sketch()
        self.assertEqual("", item.text)

    def test_item_related_with_model(self):
        """ test: Sketch model related with
            Song model
        """
        song = Song.objects.create(name="test")
        item = Sketch()
        item.song = song
        item.save()
        self.assertIn(item, song.sketch_set.all())

    def test_cannot_save_empty_sketch_on_song(self):
        """ Test cannot add empty elements in Song class """

        song = Song.objects.create()
        chunk = Sketch(song=song, text="")
        with self.assertRaises(ValidationError):
            chunk.full_clean()
            chunk.save()


    def test_Can_save_duplicate_sketch_model_items_in_different_song_models(self):
        """ Test that duplicate Sketch model can save in
            two different Song models
        """
        song1 = Song.objects.create(name="First")
        song2 = Song.objects.create(name="Second")
        Sketch.objects.create(text='Test', song=song1)
        sketch = Sketch(text='Test', song=song2)
        sketch.full_clean()

    
    def test_list_ordering(self):
        """ test: check correct ordering in the list """
        song = Song.objects.create(name="test")
        chunk1 = Sketch.objects.create(song=song, text='1')
        chunk2 = Sketch.objects.create(song=song, text='2')
        chunk3 = Sketch.objects.create(song=song, text='3')
        
        self.assertEqual(list(Sketch.objects.all()), [chunk1, chunk2, chunk3])


    def test_string_representation(self):
        """ test: string representation """
        chunk = Sketch(text="Some text")
        self.assertEqual(str(chunk), "Some text")


class MusicNoteModelTest(TestCase):
    
    def test_save_note(self):
        """ test: model save a note
        """
        a_note = MusicNote.objects.create(name='A')
        self.assertEqual(a_note.name, 'A')
        self.assertEqual(len(MusicNote.objects.all()), 1)
        # Trying to save another one
        a_sharp_note = MusicNote.objects.create(name='A#')
        self.assertEqual(len(MusicNote.objects.all()), 2)
        self.assertNotEqual(a_note.name, a_sharp_note.name)

    def test_saving_invalid_note(self):
        """ test: model cannot save invaid notes """
        correct_note = MusicNote.objects.create(name="G#")
        self.assertEqual(len(MusicNote.objects.all()), 1)

        with self.assertRaises(IntegrityError):
            incorrect_note = MusicNote.objects.create(name="Gu")

    def test_model_throw_an_error_in_trying_to_save_duplicate_note(self):
        """ test: model will throw integrity error, if we trying to save
            the same note in the table
        """
        a_note = MusicNote.objects.create(name="A")
        with self.assertRaises(IntegrityError):
            another_a_note = MusicNote.objects.create(name="A")
        


class ChordModelTest(TestCase):

    def setUp(self):
        # setup a music note table, with all valid notes
        for item in MUSIC_NOTES:
            MusicNote.objects.create(name=item)

    def test_save_chord(self):
        note = ' a '.strip().upper()
        # Check is note is valid
        root_note = MusicNote.objects.get(name=note)
        a_chord = Chord.objects.create(name='A minor', root_note=root_note)
        self.assertEqual(a_chord.name, 'A minor')
        self.assertEqual(a_chord.root_note, root_note)


class ChordNotesRelationModelTest(TestCase):

    def setUp(self):
        # setup a music note table, with all valid notes
        for item in MUSIC_NOTES:
            MusicNote.objects.create(name=item)

    def test_adding_a_chord_notes_to_chord(self):
        # Test: create new relation between chord and chord notes
        a_minor_notes = ['A', 'C', 'E']
        root = MusicNote.objects.get(name=a_minor_notes[0])
        a_chord = Chord.objects.create(name='A minor', root_note=root)
        for item in a_minor_notes:
            note = MusicNote.objects.get(name=item)
            ChordNotesRelation.objects.create(chord_name=a_chord, chord_note=note)
        # Check that we save all notes of a chord in the model        
        for note in ChordNotesRelation.objects.filter(chord_name=a_chord):
            self.assertIn(note.chord_note.name, a_minor_notes)
        self.assertEqual(len(a_minor_notes), len(ChordNotesRelation.objects.filter(chord_name=a_chord)))

    def test_throw_an_error_when_adding_duplicate_notes_in_chord(self):
        """ Test: model throw an error when adding duplicates in it """
        f_major_notes = ['F', 'A', 'C']
        root = MusicNote.objects.get(name=f_major_notes[0])
        f_maj_chord = Chord.objects.create(name='F major', root_note=root)

        with self.assertRaises(IntegrityError):
            ChordNotesRelation.objects.create(chord_name=f_maj_chord, chord_note=root)
            ChordNotesRelation.objects.create(chord_name=f_maj_chord, chord_note=root)

        
class GuitarStuffClassTest(TestCase):

    def setUp(self) -> None:
        for note in GuitarStuffClass._notes:
            MusicNote.objects.create(name=note)
        
        self.guitar = GuitarStuffClass()

        for note in MusicNote.objects.all():
            self.fill_the_chord_with_notes(note.name)


    def fill_the_chord_with_notes(self, key_note):
        root = MusicNote.objects.get(name=key_note)

        scale_from_root = self.guitar.string_tuning(root.name)

        for chord_name in self.guitar._chord_formula:
            chord, _ = Chord.objects.get_or_create(name=f"{root.name} {chord_name}", root_note=root)
            notes = self.guitar._chord_formula[chord_name]
            for note in notes:
                chord_note = MusicNote.objects.get(name=scale_from_root[note])
                ChordNotesRelation.objects.get_or_create(chord_name=chord, chord_note=chord_note)

        