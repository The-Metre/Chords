from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
    
    def wait(fn):
        def modified_fn(*args, **kwargs):
            start_time = time.time()
            while True:
                try:
                    return fn(*args, **kwargs)
                except (AssertionError, WebDriverException) as e:
                    if time.time() - start_time > MAX_WAIT:
                        raise e
                    time.sleep(0.5)
        return modified_fn
    
    @wait
    def wait_for_row_in_list_table(self, row_text):
        """ wait for row in the table """
        table = self.browser.find_element(By.ID, 'id_song_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        
        self.assertIn(row_text, [row.text for row in rows])

    @wait
    def wait_for(self, func):
        """ Wait for """
        return func()

    @wait
    def wait_to_be_logged_in(self, email):
        """ Test: login to the system
            and trying to find our email dress 
            on a page
        """
        self.browser.find_element(By.LINK_TEXT, 'Log out')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertIn(email, navbar.text)

    @wait
    def wait_to_be_logged_out(self, email):
        """ Test: log out from the system
            page should not contains our email 
        """
        self.browser.find_element(By.NAME, 'email')
        navbar = self.browser.find_element(By.CSS_SELECTOR, '.navbar')
        self.assertNotIn(email, navbar.text)


    def add_song_item(self, item_text):
        # add a new elements of the list
        num_rows = len(self.browser.find_elements(
            By.CSS_SELECTOR, '#id_song_table'))
        print(num_rows)
        self.get_song_input_box().send_keys(item_text)
        self.get_song_input_box().send_keys(Keys.ENTER)
        item_number = num_rows + 1
        self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

    def get_song_input_box(self):
        return self.browser.find_element(By.ID, 'id_name')

    def get_sketch_input_box(self):
        return self.browser.find_element(By.ID, 'id_text')

if __name__ == '__main__':
    StaticLiveServerTestCase.main(warnings='ignore')