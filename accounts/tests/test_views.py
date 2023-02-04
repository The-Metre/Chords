from django.test import TestCase
from unittest.mock import patch

class SendLoginEmailViews(TestCase):

    def test_redirect_to_home_page(self):
        """ Test: redirect to home page """
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        self.assertRedirects(response, '/')

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_adress_from_post(self, mock_send_mail):
        """ Test: sends mail on adress from post method """

        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })

        self.assertEqual(mock_send_mail.called, True)
        (subject, body, sender, to_list), kwargs = mock_send_mail.call_args
        self.assertEqual(subject, 'Your login link for Chords')
        self.assertEqual(sender, 'noreply@chords')
        self.assertEqual(to_list, ['edith@example.com'])
    