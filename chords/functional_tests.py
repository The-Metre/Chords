from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element(By.ID, 'id_song_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_new_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

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
        self.check_for_row_in_list_table('1: Group name one')
        time.sleep(1)

        
        # Try to fill the second info in form space and press 'enter' key
        inputbox = self.browser.find_element(By.ID, 'id_new_song_name')
        inputbox.send_keys('Group name second')
        inputbox.send_keys(Keys.ENTER)
        
        time.sleep(1)

        # Check the table tag and correct rows
        table = self.browser.find_element(By.ID, 'id_song_table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        
        
        self.check_for_row_in_list_table('1: Group name one')
        self.check_for_row_in_list_table('2: Group name second')
        
        self.assertIn(
            '1: Group name one', [row.text for row in rows],
            f"New element doesn't show in the table, table contain: \n{table.text}"
        )

        self.assertIn(
            '2: Group name second', [row.text for row in rows],
            f"New element doesn't show in the table, table contain: \n{table.text}"
        )

        # End of the test
        #self.fail('End of the test')

if __name__ == '__main__':
    unittest.main(warnings='ignore')