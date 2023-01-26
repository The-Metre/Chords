from django.test import TestCase
from django.core.exceptions import ValidationError

from pocket_chords.models import Song, Sketch


# Create your tests here.


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

    def test_cannot_save_empty_sketch_on_song(self):
        """ Test cannot add empty elements in Song class """

        song = Song.objects.create()
        chunk = Sketch(song=song, text="")
        with self.assertRaises(ValidationError):
            chunk.save()
            chunk.full_clean()

class SongAndSketchModelTest(TestCase):
    ''' test Sketch model '''

    def test_default_text(self):
        item = Sketch()
        self.assertEqual("", item.text)

    def test_item_related_with_model(self):
        song = Song.objects.create(name="test")
        item = Sketch()
        item.song = song
        item.save()
        self.assertIn(item, song.sketch_set.all())

    def test_duplicate_items_are_invalid_in_song_model(self):
        """ test: cannot save duplicate items in Song model """
        Song.objects.create(name="Test item")
        with self.assertRaises(ValidationError):
            new_song = Song(name="Test item")
            new_song.full_clean()

    def test_duplicate_items_are_invalid_in_sketch_model(self):
        """ test: cannot save duplicate items in Sketch model """
        song = Song.objects.create(name="Test item")
        chunk = Sketch.objects.create(text="Test sketch", song=song)
        with self.assertRaises(ValidationError):
            dup_sketch = Sketch(text="Test sketch", song=song)
            dup_sketch.full_clean()

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
        song = Song.objects.create(name="test")
        chunk1 = Sketch.objects.create(song=song, text='1')
        chunk2 = Sketch.objects.create(song=song, text='2')
        chunk3 = Sketch.objects.create(song=song, text='3')
        
        self.assertEqual(list(Sketch.objects.all()), [chunk1, chunk2, chunk3])


    def test_string_representation(self):
        chunk = Sketch(text="Some text")
        self.assertEqual(str(chunk), "Some text")