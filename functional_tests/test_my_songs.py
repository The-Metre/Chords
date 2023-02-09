from django.conf import settings
from selenium.webdriver.common.by import By
from django.contrib.auth import (
    BACKEND_SESSION_KEY, SESSION_KEY,
    get_user_model
)
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest

User = get_user_model()

class MySongsTest(FunctionalTest):
    """ Test app pocket chords """
    def create_pre_authenticated_session(self, email):
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        # Set a cookie, that we will needed for 
        # the first visiting of a domain
        self.browser.get(self.live_server_url + "/404_no_such_url/")
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def test_logged_in_users_chords_are_saved_as_my_chords(self):
        # Try to add a new 'test song' and then a 'test chuck' to the song
        self.browser.get(self.live_server_url)
        self.add_song_item('test song')

        # Store a 'test song' page url
        first_song_url = self.browser.current_url

        # Find a link to 'My songs' list and click on it
        self.browser.find_element(By.LINK_TEXT, 'My songs').click()

        # Find a link for 'test song' in 'My songs list' page
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEXT, "test song")
        )
        self.browser.find_element(By.LINK_TEXT, 'test song').click()

        # Check that urls are matched
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_song_url)
        )       

        # Add one more song list
        self.browser.get(self.live_server_url)
        self.add_song_item('second song')
        second_song_url = self.browser.current_url

        # Click a link that forward to 'My songs list'
        self.browser.find_element(By.LINK_TEXT, 'My songs').click()

        # Find the second song in a list
        self.wait_for(
            lambda: self.browser.find_element(By.LINK_TEST, 'second song')
        )
        self.browser.find_element(By.LINK_TEXT, 'second song').click()

        # Check that urls of the song are matched
        self.wait_for(
            lambda: self.assertEqual(second_song_url, self.browser.current_url)
        )

        # Log out from current session
        self.browser.find_element(By.LINK_TEXT, "Log out").click()
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_elements(By.LINK_TEXT, 'My songs', [])
            
        ))        