from django.test import TestCase
from pocket_chords.models import Song, Sketch
# Create your tests here.

class SongAndSketchModelTest(TestCase):
    ''' test Song model '''

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

class HomePageTest(TestCase):
    ''' test home page'''

    def test_uses_home_page_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'homepage.html')

    

class ListViewTest(TestCase):
    """ test to check elements in the list """

    def test_uses_songs_list_template(self):
        """ test: uses list template """
        response = self.client.get('/songs_list/something_right_here/')
        self.assertTemplateUsed(response, 'songs_list.html')

    def test_displays_all_items(self):
        """ test: all elements a shown """
        Song.objects.create(name='item 1')
        Song.objects.create(name='item 2')

        response = self.client.get('/songs_list/something_right_here/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')

class NewListVTest(TestCase):
    """ Test a new list """

    def test_can_save_a_POST_request(self):
        self.client.post('/songs_list/new', data={'song_name': 'A new list item'})

        self.assertEqual(Song.objects.count(), 1)
        new_item = Song.objects.first()
        self.assertEqual(new_item.name, 'A new list item')
    
    def test_can_redirect_after_the_POST(self):
        response = self.client.post('/songs_list/new', data={'song_name': 'A new list item'})
        self.assertRedirects(response, '/songs_list/something_right_here/')

    def test_cannot_save_empty_file(self):
        self.client.post('/songs_list/new', data={'song_name': ''})

        self.assertEqual(Song.objects.count(), 0)