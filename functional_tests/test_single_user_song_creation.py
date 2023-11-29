from .base import FunctionalTest

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class CreateNewSongTest(FunctionalTest):

    def test_can_create_a_new_song(self):
        """ test: create a new song for single user """
        url = "http://localhost:48473/accounts/login?token=907ab52f-ca45-4a2d-a25f-6e9f613cac39"

        self.browser.get(self.live_server_url)

        self.browser.get(url)

        header_text = self.browser.find_element(By.TAG_NAME, 'h1').text
        
        self.wait_to_be_logged_in(email='edit')