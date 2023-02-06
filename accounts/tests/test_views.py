from django.test import TestCase
from unittest.mock import patch, call

from accounts.models import Token


class SendLoginEmailViews(TestCase):

    def test_redirect_to_home_page(self):
        """ Test: redirect to home page """
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edith@example.com'
        })
        self.assertRedirects(response, '/')

    def test_add_success_message(self):
        response = self.client.post('/accounts/send_login_email', data={
            'email': 'edit@example.com' 
        }, follow=True)
        message = list(response.context['messages'])[0]
        
        self.assertEqual(
            message.message,
            "Check your email, we sent you a link, \
        which you can use to login into the site"
        )
        self.assertEqual(message.tags, 'success')

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
    

    @patch('accounts.views.messages')
    def test_adds_success_message_with_mocks(self, moch_messages):
            response = self.client.post('/accounts/send_login_email', data={
                 'email': 'edit@example.com'
            })

            expected = "Check your email, we sent you a link, \
        which you can use to login into the site"
            self.assertEqual(
                 moch_messages.success.call_args,
                 call(response.wsgi_request, expected),
            )

class LoginViewsTest(TestCase):
    """ test view log in to system """
     
    def test_redirect_to_home_page(self):
        response = self.client.get('/accounts/login?token=abcd123')
        self.assertRedirects(response, '/')


    def test_creates_token_associated_with_email(self):
        """ test: creates marker,
            associated with email 
        """
        self.client.post('/accounts/send_login_email', data={
             'email': 'edit@example.com'
        })
        token = Token.objects.first()
        self.assertEqual(token.email, 'edit@example.com')
    
    @patch('accounts.views.send_mail')
    def test_sends_link_to_login_using_token_uid(self, mock_send_mail):
        """ test: sends a link to log in
            system, using uid marker 
        """
        self.client.post('/accounts/send_login_email', data={
            'email': 'edit@example.com'
        })

        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, sender, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)