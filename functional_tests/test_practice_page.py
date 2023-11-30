from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from .base import FunctionalTest



FIRST_TEST_EMAIL = 'firstone@example.com'

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



    def test_render_practice_page(self):
        """ check that browser render practice page
            when click on the button on the main page
        """

        self.browser.get(self.live_server_url)
        a = self.browser.find_element(By.ID, 'logout-button')
        print(a.text)
      