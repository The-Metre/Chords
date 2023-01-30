from django.test import TestCase
from pocket_chords.forms import (
    SongForm, SketchForm,
    EMPTY__ITEM_ERROR, DUPLICATE_ITEM_ERROR
    )
from pocket_chords.models import Song, Sketch

# Sample of Song object for tests
def create_test_song():
        return Song.objects.create(name='test')


class SongFormTest(TestCase):
    """ Test: form of Song model """

    def test_form_renders_song_text_input(self):
        """ test: check that form renders on page """
        form = SongForm()
        self.assertIn('placeholder="Enter an item', form.as_p())
        self.assertIn('class="form-control input-lg', form.as_p())

    def test_validation_for_blank_items(self):
        """ test: validations blank form item """
        form = SongForm(data={'name':""})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['name'],
            [EMPTY__ITEM_ERROR]
        )


class SketchFormTest(TestCase):
    """ Test: form of Sketch model """

    def test_form_render_sketch_text_input(self):
        """ test: check that Sketch form
            renders on page
        """
        form = SketchForm()
        self.assertIn('placeholder="Enter a song item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())


    def test_validation_for_blank_items(self):
        """ test: validations blank form item """
        song = create_test_song()
        form = SketchForm(data={'text': "", 'song': song})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY__ITEM_ERROR]
        )
    
    def test_duplicate_items_save_in_the_save_model(self):
        """ test: saving duplicate item in
            the same model
        """
        song = create_test_song()
        sketch = Sketch.objects.create(text='dup', song=song)
        form = SketchForm(data={'text': 'dup', "song": song})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["__all__"],
            [DUPLICATE_ITEM_ERROR]
        )