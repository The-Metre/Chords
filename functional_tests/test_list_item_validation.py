from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest import skip


class ItemValidationTest(FunctionalTest):


    def test_cannot_create_empty_list(self):
        """ Test cannot create an empty list """
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, 'id_new_song_name').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
            "You can't have an empty song name field"
        )) 

        song_name = "Test new song name"
        self.browser.find_element(By.ID, 'id_new_song_name').send_keys(song_name)
        self.browser.find_element(By.ID, 'id_new_song_name').send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.TAG_NAME, 'h1').text,
            f"Your Music List for ({song_name})"
        ))

    def test_cannot_add_empty_item_to_a_list(self):
        """ Test cannot add empty element in the list """
        self.browser.get(self.live_server_url)
        self.browser.find_element(By.ID, 'id_new_song_name').send_keys("Test song")
        self.browser.find_element(By.ID, 'id_new_song_name').send_keys(Keys.ENTER)

        self.browser.find_element(By.ID, 'id_new_song_chunk').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
            "You can't have an empty song item field"
        ))

        first_chunk_text = "Test chunk"
        second_chunk_text = "Test another chunk"

        self.browser.find_element(By.ID, 'id_new_song_chunk').send_keys(first_chunk_text)
        self.browser.find_element(By.ID, 'id_new_song_chunk').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(f"1: {first_chunk_text}")

        self.browser.find_element(By.ID, 'id_new_song_chunk').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.CSS_SELECTOR, '.has-error').text,
            "You can't have an empty song item field"
        ))

        self.browser.find_element(By.ID, 'id_new_song_chunk').send_keys(second_chunk_text)
        self.browser.find_element(By.ID, 'id_new_song_chunk').send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table(f"1: {first_chunk_text}")
        self.wait_for_row_in_list_table(f"2: {second_chunk_text}")

    def end(self):
        self.fail("End of the tests")

        
if __name__ == '__main__':
    pass