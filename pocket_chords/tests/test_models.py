from django.test import TestCase
from django.core.exceptions import ValidationError

from pocket_chords.models import Song, Sketch


# Create your tests here.

class SongAndSketchModelTest(TestCase):
    ''' test Song and Sketch models '''

    def test_saving_and_retrieving_items(self):
        song = Song()
        song.save()

        first_item = Sketch()
        first_item.text = 'The first(ever) list item'
        first_item.song = song
        first_item.save()
        

        second_item = Sketch()
        second_item.text = 'Item the second'
        second_item.song = song
        second_item.save()


        saved_song = Song.objects.first()
        self.assertEqual(saved_song, song)

        saved_items = Sketch.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.song, song)
        self.assertEqual(first_saved_item.text, 'The first(ever) list item')
        self.assertEqual(second_saved_item.song, song)
        self.assertEqual(second_saved_item.text, 'Item the second')


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

    def test_get_absolute_url(self):
        """ Test: handeled absolute url"""

        song = Song.objects.create(name="test song")
        self.assertEqual(song.get_absolute_url(), f'/song_page/{song.id}/')

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
