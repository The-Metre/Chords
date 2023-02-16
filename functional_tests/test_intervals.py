from .base import FunctionalTest
from selenium.webdriver.common.by import By


class IntervalPageTest(FunctionalTest):

    def test_can_redirect_to_intervals_page_from_homepage(self):
        # Open browser at the homepage
        self.browser.get(self.live_server_url)

        # Find a redirection link on the page
        # and click on it
        self.browser.find_element(By.LINK_TEXT, "Intervals").click()

        # Make sure that we redirected on correct url
        self.wait_for(
            lambda: self.assertEquals(self.live_server_url, '/intervals')
        )
