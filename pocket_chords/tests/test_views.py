from django.test import TestCase
from django.utils.html import escape

from pocket_chords.models import Song, Sketch
from pocket_chords.forms import SongForm


# Create your tests here.

class HomePageTest(TestCase):
    ''' test home page'''

    def test_uses_home_page_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'homepage.html')
    
    def test_home_page_uses_song_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], SongForm)
        

class ListViewTest(TestCase):
    """ test to check elements in the list """

    def test_uses_songs_list_template(self):
        """ test: uses list template """
        song = Song.objects.create(name="Test song")
        response = self.client.get(f'/song_page/{song.id}/')
        self.assertTemplateUsed(response, 'song_page.html')

    def test_displays_all_items(self):
        """ test: all elements a shown """
        correct_song = Song.objects.create(name="Test song")

        Sketch.objects.create(text='item 1', song=correct_song)
        Sketch.objects.create(text='item 2', song=correct_song)

        other_song = Song.objects.create(name="Other song")
        
        Sketch.objects.create(text='other song item 1', song=other_song)
        Sketch.objects.create(text='other song item 2', song=other_song)

        response = self.client.get(f'/song_page/{correct_song.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'other song item 1')
        self.assertNotContains(response, 'other song item 2')

    def test_passes_correct_song_to_template(self):
        other_song = Song.objects.create(name='other song')
        correct_song = Song.objects.create(name='correct song')
        response = self.client.get(f'/song_page/{correct_song.id}/')
        self.assertEqual(response.context['song'], correct_song)

    
    def test_can_redirect_after_the_POST(self):
        response = self.client.post('/song_page/new', data={'name': 'A new list item'})
        new_song = Song.objects.first()
        self.assertRedirects(response, f'/song_page/{new_song.id}/')

    def test_can_save_a_POST_request_to_existing_song(self):
        other_song = Song.objects.create(name='Other song')
        correct_song = Song.objects.create(name='Correct Song')

        self.client.post(
                    f'/song_page/{correct_song.id}/',
                    data={'name': 'A new chunk to existing song'})
            
        self.assertEqual(Sketch.objects.count(), 1)
        new_item = Sketch.objects.first()

        self.assertEqual(new_item.text, 'A new chunk to existing song')
        self.assertEqual(new_item.song, correct_song)

    def test_validation_errors_are_send_back_to_homepage_template(self):
        response = self.client.post('/song_page/new', data={'name': ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
        expected_error = escape("You can't save an empty song item")

        self.assertContains(response, expected_error)

    def test_invalid_song_item_arent_saved(self):
        self.client.post('/song_page/new', data={'name': ""})
        self.assertEqual(Song.objects.count(), 0)
        self.assertEqual(Sketch.objects.count(), 0)

    def test_validation_errors_end_up_on_song_page(self):
        song = Song.objects.create(name="test song")
        response = self.client.post(
            f'/song_page/{song.id}/',
            data={'name': ""}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'song_page.html')
        expected_error = escape("You can't save an empty song item")
        self.assertContains(response, expected_error)