from django.test import TestCase
# Create your tests here.

class HomePageTest(TestCase):
    ''' test home page'''

    def test_uses_home_page_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'homepage.html')
    
    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'song_name': 'A new list item'})
        self.assertIn('A new list item', response.content.decode())
        self.assertTemplateUsed(response, 'homepage.html')