from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest


FIRST_TEST_EMAIL = 'firstone@example.com'
SECOND_TEST_EMAIL = 'anothermail@example.com'

SUBJECT = 'Your login link for Chords'

class LoginTest(FunctionalTest):
    """ Test multiple loggin
    """
    def setUp(self) -> None:
        """ Standart setup, plus login with FIRST_TEST_EMAIL 
        """
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(options=self.options)


        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(FIRST_TEST_EMAIL)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        email = mail.outbox[0]
        url_search = re.search(r'http://.+/.+$', email.body)
        url = url_search.group(0)
        self.browser.get(url)

    def tearDown(self) -> None:
        self.browser.quit()


    def test_can_login_single_user(self):
        """ Check that setup works properly """
        first_email_username, _ = FIRST_TEST_EMAIL.split('@')
        self.wait_to_be_logged_in(email=first_email_username)

    def test_can_relogin_with_different_user(self):
        """ Test that we can login under the different username """
        # Logout as first user
        self.browser.find_element(By.ID, 'logout-button').click()
        try:
            # Check that after we logout, navbar will be hidden
            loged_first_user_name_text = self.browser.find_element(By.CLASS_NAME, 'navbar-text').text
        except NoSuchElementException:
            loged_first_user_name_text = ""
        first_username, _ = FIRST_TEST_EMAIL.split('@')
        # Check that navbar doesn't show at the page
        self.assertNotIn(first_username, loged_first_user_name_text)

        # Login under the second user
        self.browser.find_element(By.NAME, 'email').send_keys(SECOND_TEST_EMAIL)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)
        second_email_username, _ = SECOND_TEST_EMAIL.split('@')
        email = mail.outbox[1]
        url_search = re.search(r'http://.+/.+$', email.body)
        url = url_search.group(0)
        self.browser.get(url)
        # Check that logout button is show
        self.wait_to_be_logged_in(email=second_email_username)
        loged_second_user_name_text = self.browser.find_element(By.CLASS_NAME, 'navbar-text').text
        # Check that login under the different user
        self.assertNotEqual(loged_first_user_name_text, loged_second_user_name_text)