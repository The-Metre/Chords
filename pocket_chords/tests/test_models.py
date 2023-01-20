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