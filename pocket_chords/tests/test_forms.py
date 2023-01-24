from django.test import TestCase
from pocket_chords.forms import SongForm, EMPTY__ITEM_ERROR
from pocket_chords.models import Song, Sketch


class SongFormTest(TestCase):

    def test_form_renders_song_text_input(self):
        form = SongForm()
        self.assertIn('placeholder="Enter an item', form.as_p())
        self.assertIn('class="form-control input-lg', form.as_p())

    def test_validation_for_blank_items(self):
        form = SongForm(data={'name':""})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['name'],
            [EMPTY__ITEM_ERROR]
        )



