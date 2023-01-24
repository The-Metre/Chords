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
        self.options.add_argument('--no-samdbox')
        self.options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(options=self.options)
        time.sleep(MAX_WAIT)

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


    def get_item_input_box(self):
        return self.browser.find_element(By.ID, 'id_name')


if __name__ == '__main__':
    StaticLiveServerTestCase.main(warnings='ignore')