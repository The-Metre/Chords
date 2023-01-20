from django.test import TestCase
from pocket_chords.models import Song, Sketch
# Create your tests here.

class HomePageTest(TestCase):
    ''' test home page'''

    def test_uses_home_page_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'homepage.html')

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

class NewListVTest(TestCase):
    """ Test a new list """

    def test_can_save_a_POST_request(self):
        self.client.post('/song_page/new', data={'song_name': 'A new list item'})

        self.assertEqual(Song.objects.count(), 1)
        new_item = Song.objects.first()
        self.assertEqual(new_item.name, 'A new list item')
    
    def test_can_redirect_after_the_POST(self):
        response = self.client.post('/song_page/new', data={'song_name': 'A new list item'})
        new_song = Song.objects.first()
        self.assertRedirects(response, f'/song_page/{new_song.id}/')

    def test_can_save_a_POST_request_to_existing_song(self):
        other_song = Song.objects.create(name='Other song')
        correct_song = Song.objects.create(name='Correct Song')

        self.client.post(
                    f'/song_page/{correct_song.id}/add_item',
                    data={'chunk': 'A new chunk to existing song'})
            
        self.assertEqual(Sketch.objects.count(), 1)
        new_item = Sketch.objects.first()

        self.assertEqual(new_item.text, 'A new chunk to existing song')
        self.assertEqual(new_item.song, correct_song)


    def test_redirect_to_song_view(self):
        other_song = Song.objects.create(name="test song")
        correct_song = Song.objects.create(name='correct_test_song')

        response = self.client.post(
                        f'/song_page/{correct_song.id}/add_item',
                        data={'chunk': 'A new item to existing song'}
        )
        self.assertRedirects(response, f'/song_page/{correct_song.id}/')

    def test_cannot_save_empty_file(self):
        self.client.post('/song_page/new', data={'song_name': ''})

        self.assertEqual(Song.objects.count(), 0)