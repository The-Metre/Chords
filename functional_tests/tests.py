from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import time



MAX_WAIT  = 10

class NewVisitorTest(LiveServerTestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self,    row_text):
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

    def test_can_start_a_list_for_one_user(self):
        """ test:
                create a list of songs for single user
        """
        self.browser.get(self.live_server_url)

        # Check the correct title
        self.assertIn('To-Do', self.browser.title)

        # Check header
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text

        self.assertIn('Music', header_text)

        # Check the correct input tag
        inputbox = self.browser.find_element(By.ID, 'id_new_song_name')
        
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a song name'
        )
        
        # Try to fill the info in form space and press 'enter' key
        inputbox.send_keys('Group name one')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Group name one')

        
        # Try to fill the second info in form space and press 'enter' key
        inputbox = self.browser.find_element(By.ID, 'id_new_song_name')
        inputbox.send_keys('Group name second')
        inputbox.send_keys(Keys.ENTER)
        
        
        self.wait_for_row_in_list_table('1: Group name one')
        self.wait_for_row_in_list_table('2: Group name second')
        
        # End of the test
        #self.fail('End of the test')

if __name__ == '__main__':
    LiveServerTestCase.main(warnings='ignore')