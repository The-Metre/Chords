from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest import skip


class ItemValidationTest(FunctionalTest):


    def test_cannot_create_empty_list(self):
        """ Test cannot create an empty list """
        self.browser.get(self.live_server_url)
        self.get_song_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.browser.find_element(
                By.CSS_SELECTOR, '#id_name:invalid'
        ))


    def test_cannot_add_empty_item_to_a_list(self):
        """ Test cannot add empty element in the Song list """
        self.browser.get(self.live_server_url)
        self.get_song_input_box().send_keys("Test song")
        self.get_song_input_box().send_keys(Keys.ENTER)

        self.get_sketch_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element(
                By.CSS_SELECTOR, '#id_text:invalid'
        ))

        first_chunk_text = "Test chunk"
        second_chunk_text = "Test another chunk"

        self.get_sketch_input_box().send_keys(first_chunk_text)
        self.get_sketch_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table(f"1: {first_chunk_text}")

        self.get_sketch_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element(
                By.CSS_SELECTOR, '#id_text:invalid'
        ))

        self.get_sketch_input_box().send_keys(second_chunk_text)
        self.get_sketch_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table(f"1: {first_chunk_text}")
        self.wait_for_row_in_list_table(f"2: {second_chunk_text}")

    def test_cannot_add_duplicate_values(self):
        """ test: user cannot add duplicate values
            in a form
        """

        # Add item in a form
        self.browser.get(self.live_server_url)
        self.get_song_input_box().send_keys('Test Song')
        self.get_song_input_box().send_keys(Keys.ENTER)

        self.get_sketch_input_box().send_keys('Test 1')
        self.get_sketch_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Test 1')

        # Add the same item again
        self.get_sketch_input_box().send_keys('Test 1')
        self.get_sketch_input_box().send_keys(Keys.ENTER)

        # Check that error message appear
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element(By.TAG_NAME, 'li').text,
            "Item already exists in the model"
        ))

    