from django.test import TestCase
from django.urls import resolve

from pocket_chords.views import home_page
# Create your tests here.

class HomePageTest(TestCase):
    ''' test home page'''

    def test_root_url_resolved_to_home_page_view(self):
        found = resolve('/')

        self.assertEqual(found.func, home_page)