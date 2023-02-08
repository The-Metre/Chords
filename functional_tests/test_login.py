from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re


from .base import FunctionalTest

TEST_EMAIL = 'edit@example.com'
SUBJECT = 'Your login link for Chords'

class LoginTest(FunctionalTest):
    """ Test login on a system """

    def test_can_get_email_link_to_log_in(self):
        """ Test: can get link on an email 
            for registration
        """
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        # Show a message that an email was sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element(By.TAG_NAME, 'body').text
        ))

        # User check his mailbox
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # The email contain link on url-adress
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # User click on the link
        self.browser.get(url)

        # User is registered in the system
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Log out')
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar').text
        self.assertIn(TEST_EMAIL, navbar)

    
    def test_can_get_email_link_to_log_in(self):
        """ test: can get a link
            in mailbox from registration
        """
        self.wait_to_be_logged_in(email=TEST_EMAIL)
        self.browser.find_element(By.LINK_TEXT, 'Log out').click()
        self.wait_to_be_logged_out(email=TEST_EMAIL)