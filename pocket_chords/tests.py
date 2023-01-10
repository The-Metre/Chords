from django.test import TestCase
# Create your tests here.

class HomePageTest(TestCase):
    ''' test home page'''

    def test_uses_home_page_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'homepage.html')