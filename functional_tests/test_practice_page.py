from django.core import mail
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

from .base import FunctionalTest



"""  """
from pocket_chords.models import MusicNote, Chord, ChordNotesRelation
from project_tools.classes import GuitarStuffClass
"""  """

TEST_EMAIL = 'firstone@example.com'
TEST_FIRST_CHORD_NAME = 'a minor'
TEST_SECOND_CHORD_NAME = 'f major'
TEST_FIRST_CHORD_NOTES = 'A C E'
TEST_SECOND_CHORD_NOTES = 'F A C'
EMAIL_USERNAME, _ = TEST_EMAIL.split('@')
# Values to test metronome tempo changes
DEFAULT_METRONOME_TEMPO = 140
PLUS_TEMPO = 3
MINUS_TEMPO = 11
# Values to test metronome measure
DEFAULT_METRONOME_MEASURE_COUNT_VALUE = 4
ADD_MEASURE = 2
SUBTRACT_MEASURE = 3

class LoginTest(FunctionalTest):
    """ Test multiple loggin
    """
    def setUp(self) -> None:
        """ Standart setup, plus login with FIRST_TEST_EMAIL 
        """
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(options=self.options)


        self.browser.get(self.live_server_url)
        self.browser.find_element(By.NAME, 'email').send_keys(TEST_EMAIL)
        self.browser.find_element(By.NAME, 'email').send_keys(Keys.ENTER)

        email = mail.outbox[0]
        url_search = re.search(r'http://.+/.+$', email.body)
        url = url_search.group(0)
        self.browser.get(url)

    def tearDown(self) -> None:
        self.browser.quit()


    def to_practice_page(fn):
        """
        Decorator to redirect to the practice page
        """
        def modified_fn(self, *args, **kwargs):
            # open a practice page
            self.wait_for(self.browser.find_element(By.LINK_TEXT, 'Practice').click)
            return fn(self, *args, **kwargs)
        return modified_fn
    

    def _fill_the_chord_with_notes(self, key_note):
        """ 
        function to fill music class object with notes
        """
        root = MusicNote.objects.get(name=key_note)
        scale_from_root = self.guitar.string_tuning(root.name)

        for chord_name in self.guitar._chord_formula:
            # Fill Chord sql table with chord name and related root note
            chord, _ = Chord.objects.get_or_create(name=f"{root.name} {chord_name}", root_note=root)
            notes = self.guitar._chord_formula[chord_name]
            for note in notes:
                # Fill Chord-Notes relationship table
                chord_note = MusicNote.objects.get(name=scale_from_root[note])
                ChordNotesRelation.objects.get_or_create(chord_name=chord, chord_note=chord_note)

    def test_render_practice_page(self):
        """ check that browser render practice page
            when click on the button on the main page
        """
        # start on the main page
        main_page_url = self.live_server_url
        practice_page_link = self.browser.find_element(By.LINK_TEXT, 'Practice')
        # click on the practice button
        self.wait_for(practice_page_link.click)
        # check if we redirect to a page
        self.assertNotEqual(main_page_url, self.browser.current_url)

    @to_practice_page
    def test_render_current_user_practice_page(self):
        """
        check that link redirect to the current user practice page 
        """
        # check that redirect on the current user practice page
        self.assertRegex(self.browser.current_url, f'/practice/{EMAIL_USERNAME}.+')
    
    @to_practice_page
    def test_not_render_current_user_practice_page(self):
        """
        check that link don't redirect to the current user practice page 
        """
        link_button = self.browser.find_element(By.LINK_TEXT, "My songs")
        self.wait_for(link_button.click)
        # check that not redirect on the current user practice page
        self.assertNotRegexpMatches(self.browser.current_url, f'/pracice/{EMAIL_USERNAME}.+')

    @to_practice_page
    def test_fretboard_appearance(self):
        """ 
        test visibility of a fretboard when click on checkbox
        """
        checkbox = self.browser.find_element(By.ID, 'show-guitar-fretboard')
        fretboard = self.browser.find_element(By.CLASS_NAME, 'fretboard')
        # checkbox attribute 'checked' by default should be true
        self.assertTrue(checkbox.get_attribute('checked'))
        # fretboard is visible
        self.assertTrue(fretboard.is_displayed())
        # click on the checkbox
        self.wait_for(checkbox.click)
        # fretboard should be hide
        self.assertFalse(checkbox.get_attribute('checked'))
        self.assertFalse(fretboard.is_displayed())
    
    @to_practice_page
    def test_metronome_appearance(self):
        """ 
        test visibility of a metronome on a practice page
        """
        metronome_checkbox = self.browser.find_element(By.ID, 'show-metronome')
        metronome = self.browser.find_element(By.CLASS_NAME, 'metronome')
        # by default metronome is disabled on the page
        self.assertFalse(metronome.is_displayed())
        # click on the checkbox
        self.wait_for(metronome_checkbox.click)
        # check a visibility of the metronome
        self.assertTrue(metronome.is_displayed())
    
    @to_practice_page
    def test_metronome_tempo_changes(self):
        """ 
        test tempo changes by using adjust tempo buttons
        """
        self.wait_for(self.browser.find_element(By.ID, 'show-metronome').click)
        increase_tempo_button = self.browser.find_element(By.CLASS_NAME, 'increase-tempo')
        decrease_tempo_buttom = self.browser.find_element(By.CLASS_NAME, 'decrease-tempo')
        # check default value
        self.assertEqual(DEFAULT_METRONOME_TEMPO, int(self.browser.find_element(By.CLASS_NAME, 'tempo').text))
        # increase tempo
        for _ in range(PLUS_TEMPO):
            self.wait_for(increase_tempo_button.click)
        # check that the value of a tempo is changed
        self.assertEqual(DEFAULT_METRONOME_TEMPO + PLUS_TEMPO, int(self.browser.find_element(By.CLASS_NAME, 'tempo').text))
        # decrease tempo
        for _ in range(MINUS_TEMPO):
            self.wait_for(decrease_tempo_buttom.click)
        # check that the value of a tempo is changed
        self.assertEqual(DEFAULT_METRONOME_TEMPO + PLUS_TEMPO - MINUS_TEMPO, int(self.browser.find_element(By.CLASS_NAME, 'tempo').text))

    @to_practice_page
    def test_measure_count_changes(self):
        """ 
        test changing measures count on the practice page
        """
        self.wait_for(self.browser.find_element(By.ID, 'show-metronome').click)
        add_measure_button = self.browser.find_element(By.CLASS_NAME, 'add-beats')
        subtract_measure_button = self.browser.find_element(By.CLASS_NAME, 'subtract-beats')
        # check default value
        self.assertEqual(DEFAULT_METRONOME_MEASURE_COUNT_VALUE, int(self.browser.find_element(By.CLASS_NAME, 'measure-count').text))
        # add measures of tempo
        for _ in range(ADD_MEASURE):
            self.wait_for(add_measure_button.click)
        # check that measures changed
        self.assertEqual(DEFAULT_METRONOME_MEASURE_COUNT_VALUE + ADD_MEASURE, int(self.browser.find_element(By.CLASS_NAME, 'measure-count').text))
        # subreact measures of tempo
        for _ in range(SUBTRACT_MEASURE):
            self.wait_for(subtract_measure_button.click)
        self.assertEqual(DEFAULT_METRONOME_MEASURE_COUNT_VALUE + ADD_MEASURE - SUBTRACT_MEASURE, int(self.browser.find_element(By.CLASS_NAME, 'measure-count').text))

    """ TODo """
    def test_autocomplete_input(self):
        """ 
        test autocomplete input functionality of the practice page
        """
        # setup the postgres for the test
        self.guitar = GuitarStuffClass()
        # Fill MusicNote table with all note names
        for note in self.guitar._notes:
            MusicNote.objects.get_or_create(name=note)

        # For each created note, create a related chord
        for note in MusicNote.objects.all():
            self._fill_the_chord_with_notes(note.name)


        # open a practice page
        self.wait_for(self.browser.find_element(By.LINK_TEXT, 'Practice').click)
        div_with_chord_notes = self.browser.find_element(By.CLASS_NAME, 'chord-notes')
        # type a chord name in the input field
        input_box = self.browser.find_element(By.ID, 'autocomplete-input')
        input_box.send_keys(TEST_FIRST_CHORD_NAME)
        input_box.send_keys(Keys.ENTER)
        # check correct output
        self.assertEqual(div_with_chord_notes.text, TEST_FIRST_CHORD_NOTES)
        # type a different chord name in the input field
        input_box.clear()
        input_box.send_keys(TEST_SECOND_CHORD_NAME)
        input_box.send_keys(Keys.ENTER)
        self.assertEqual(div_with_chord_notes.text, TEST_SECOND_CHORD_NOTES)


