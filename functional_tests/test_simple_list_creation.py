from .base import FunctionalTest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(FunctionalTest):

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
        inputbox = self.get_song_input_box()
        
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter an item'
        )
        
        # Try to fill the info in form space and press 'enter' key
        song_name = 'Song name One'
        inputbox.send_keys(f'{song_name}')
        inputbox.send_keys(Keys.ENTER)
        
        # Check that we redirect to correct song page
        inputbox = self.browser.find_element(By.TAG_NAME, 'h1').text

        self.assertIn(f'Add Song to your Music List', inputbox)

        # Add a new item chunk to the song list
        inputbox = self.get_song_input_box()
        
        # Check that inputbox centered
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter an item'
        )

        inputbox.send_keys('First chunk')
        inputbox.send_keys(Keys.ENTER)

      #  self.wait_for_row_in_list_table('1: First chunk')

        # Try to fill the second info in form space and press 'enter' key
        inputbox = self.get_song_input_box()
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
        inputbox = self.get_song_input_box()
        song_name = 'First user song'
        inputbox.send_keys(f'{song_name}')
        inputbox.send_keys(Keys.ENTER)

        # Check that we redirected to a correct one song

        inputbox = self.browser.find_element(By.TAG_NAME, 'h1').text
        
        self.assertEqual(inputbox, f'Add Song to your Music List')

        # Add a first item to the song
        inputbox = self.get_song_input_box()
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

        # Add a song  for the second user 
        self.browser.get(self.live_server_url)

        inputbox = self.get_song_input_box()
        song_name = 'Second user song'
        inputbox.send_keys(f'{song_name}')
        inputbox.send_keys(Keys.ENTER)

        # New user starts to add new elements in the list
        inputbox = self.get_song_input_box()
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



if __name__ == '__main__':
    pass