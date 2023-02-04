from django.test import TestCase
import accounts.views

class SendLoginEmailViews(TestCase):

    def test_redirect_to_home_page(self):
        """ Test: redirect to home page """
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        self.assertRedirects(response, '/')

    def test_sends_mail_to_adress_from_post(self):
        """ Test: sends mail on adress from post method """
        self.send_mail_called = False

        def fake_send_mail(subject, body, sender, to_list):
            """ Fake function send_email """
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.sender = sender
            self.to_list = to_list

        accounts.views.send_mail = fake_send_mail

        self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })

        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Your login link for Chords')
        self.assertEqual(self.sender, 'noreply@chords')
        self.assertEqual(self.to_list, ['edith@example.com'])
    