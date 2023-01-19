from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

import time
import os


MAX_WAIT  = 5

class NewVisitorTest(StaticLiveServerTestCase):

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



    def test_can_start_a_list_for_one_user(self):
        """ test:
                create a list of songs for single user
        """
        self.browser.get(self.live_server_url)

        # Check the correct title
        self.assertIn('Pocket Chords', self.browser.title)

        # Check header
        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text

        self.assertIn('Add Song to your Music List', header_text)


        # Check the correct input tag and placeholder
        inputbox = self.browser.find_element(By.ID, 'id_new_song_name')
        
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a song name'
        )
        
        # Try to fill the info in form space and press 'enter' key
        song_name = 'Song name One'
        inputbox.send_keys(f'{song_name}')
        inputbox.send_keys(Keys.ENTER)
        
        # Check that we redirect to correct song page
        inputbox = self.browser.find_element(By.TAG_NAME, 'h1').text

        self.assertIn(f'Your Music List for ({song_name})', inputbox)



        # Add a new item chunk to the song list
        inputbox = self.browser.find_element(By.ID, 'id_new_song_chunk')
        
        # Check that inputbox centered

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=60
        )

        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a song chunk'
        )

        inputbox.send_keys('First chunk')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: First chunk')

        
        # Try to fill the second info in form space and press 'enter' key
        inputbox = self.browser.find_element(By.ID, 'id_new_song_chunk')
        inputbox.send_keys('Second chunk')
        inputbox.send_keys(Keys.ENTER)
        
        
        self.wait_for_row_in_list_table('1: First chunk')
        self.wait_for_row_in_list_table('2: Second chunk')
        

    def test_multiple_users_can_start_lists_at_different_urls(self):
        """ test:
                multiple users can create their own lists of songs
                at different urls
        """
        # Start new list
        self.browser.get(self.live_server_url)

        # Add a song
        inputbox = self.browser.find_element(By.ID, 'id_new_song_name')
        song_name = 'First user song'
        inputbox.send_keys(f'{song_name}')
        inputbox.send_keys(Keys.ENTER)

        # Check that we redirected to a correct one song

        inputbox = self.browser.find_element(By.TAG_NAME, 'h1').text
        
        self.assertEqual(inputbox, f'Your Music List for ({song_name})')

        # Add a first item to the song
        inputbox = self.browser.find_element(By.ID, 'id_new_song_chunk')
        inputbox.send_keys('First user song chunk')
        inputbox.send_keys(Keys.ENTER)
        
        self.wait_for_row_in_list_table('1: First user song chunk')

        # Check for the user unique url
        user_number_one_url = self.browser.current_url
        self.assertRegex(user_number_one_url, '/song_page/.+')

        # Close current user session
        self.browser.quit()

        # Start new session with a new user
        self.browser = webdriver.Chrome()

        # Open a starting page, and make sure that there is nothing in it
        # from previous user
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('First user song', page_text)
        self.assertNotIn('Firds user second song', page_text)

        # Add a song  for the second user 
        inputbox = self.browser.find_element(By.ID, 'id_new_song_name')
        song_name = 'Second user song'
        inputbox.send_keys(f'{song_name}')
        inputbox.send_keys(Keys.ENTER)

        # New user starts to add new elements in the list
        inputbox = self.browser.find_element(By.ID, 'id_new_song_chunk')
        inputbox.send_keys('Second user song')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Second user song')
        
        # Check that the user get his own unique url
        user_number_two_url = self.browser.current_url
        self.assertRegex(user_number_two_url, '/song_page/.+')
        self.assertNotEqual(user_number_one_url, user_number_two_url)

        # Check that the second  user still cannot see the list
        # of the first user
        page_text = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertNotIn('First user song', page_text)
        self.assertIn('Second user song', page_text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element(By.ID, 'id_new_song_name')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=60
        )

        # End of the test
        self.fail('End of the test')

if __name__ == '__main__':
    StaticLiveServerTestCase.main(warnings='ignore')