from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
import time
import os


MAX_WAIT  = 5

class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

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


if __name__ == '__main__':
    StaticLiveServerTestCase.main(warnings='ignore')