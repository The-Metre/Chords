from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import os


MAX_WAIT  = 5

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(options=self.options)

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        """ wait for row in the table """
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, 'id_song_table')
                rows = table.find_elements(By.TAG_NAME, 'tr')
                
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as err:
                if time.time() - start_time > MAX_WAIT:
                    raise err
                time.sleep(0.5)

    def wait_for(self, func):
        """ Wait for """
        start_time = time.time()
        while True:
            try:
                return func()
            except(AssertionError, WebDriverException) as err:
                if time.time() - start_time > MAX_WAIT:
                    raise err
                time.sleep(0.5)

    def wait_to_be_logged_in(self, email):
        """ Test: login to the system
            and trying to find our email dress 
            on a page
        """
        print(self.browser)
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, 'Log out')
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)

    def wait_to_be_logged_out(self, email):
        """ Test: log out from the system
            page should not contains our email 
        """
        self.wait_for(
            lambda: self.browser.find_element(By.NAME, 'email')
        )
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)


    def get_song_input_box(self):
        return self.browser.find_element(By.ID, 'id_name')

    def get_sketch_input_box(self):
        return self.browser.find_element(By.ID, 'id_text')

if __name__ == '__main__':
    StaticLiveServerTestCase.main(warnings='ignore')