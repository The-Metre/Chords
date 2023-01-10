from django.test import TestCase
from pocket_chords.models import Song
# Create your tests here.

class SongModelTest(TestCase):
    ''' test Song model '''

    def test_saving_and_retrieving_items(self):
        first_item = Song()
        first_item.text = 'The first(ever) list item'
        first_item.save()

        second_item = Song()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Song.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first(ever) list item')
        self.assertEqual(second_saved_item.text, 'Item the second')

class HomePageTest(TestCase):
    ''' test home page'''

    def test_uses_home_page_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'homepage.html')
    
    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'song_name': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'homepage.html')