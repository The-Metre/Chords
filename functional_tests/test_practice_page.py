from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest



TEST_EMAIL = 'firstone@example.com'
EMAIL_USERNAME, _ = TEST_EMAIL.split('@')

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
        self.browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        email = mail.outbox[0]
        url_search = re.search(r'http://.+/.+$', email.body)
        url = url_search.group(0)
        self.browser.get(url)

    def tearDown(self) -> None:
        self.browser.quit()



    def test_render_practice_page(self):
        """ check that browser render practice page
            when click on the button on the main page
        """
        # start on the main page
        main_page_url = self.live_server_url
        practice_page_link = self.browser.find_element(By.LINK_TEXT, 'Practice')
        # click on the practice button
        self.wait_for(practice_page_link.click)
        # check if we redirect to a page
        self.assertNotEqual(main_page_url, self.browser.current_url)

    
    def test_render_current_user_practice_page(self):
        """
        check that link redirect to the current user practice page 
        """
        link_button = self.browser.find_element(By.LINK_TEXT, 'Practice')
        self.wait_for(link_button.click)
        # check that redirect on the current user practice page
        self.assertRegex(self.browser.current_url, f'/practice/{EMAIL_USERNAME}.+')
