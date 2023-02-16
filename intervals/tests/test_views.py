from django.test import TestCase

# Create your tests here.

class IntervalPageTest(TestCase):

    def test_uses_interval_page_template(self):
        """ test: page uses interval.html template """
        response = self.client.get('/intervals')

        self.assertTemplateUsed(response, 'intervals.html')
    