from django.test import TestCase
from django.utils.html import escape
from django.contrib.auth import get_user_model

import unittest
from unittest.mock import patch, Mock
from django.http import HttpRequest
from pocket_chords.views import new_song2 

from pocket_chords.models import Song, Sketch
from pocket_chords.forms import (
    SongForm, SketchForm,
    EMPTY__ITEM_ERROR
)

# Create your tests here.

User = get_user_model()

class HomePageTest(TestCase):
    ''' test home page'''

    def test_uses_home_page_template(self):
        response = self.client.get('/')

        self.assertTemplateUsed(response, 'homepage.html')
    
    def test_home_page_uses_song_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], SongForm)
        

class SongViewTest(TestCase):
    """ test to check elements in the list """
    def post_invalid_chunk_input(self):
        """ send an invalid input """
        song = Song.objects.create(name="test song")
        return self.client.post(f"/song_page/{song.id}/",data={'name': ""})
    
    def post_ivalid_song_input(self):
        return self.client.post('/song_page/new', data={'name': ""})

    def test_displays_item_form(self):
        song = Song.objects.create(name="Test song")
        response = self.client.get(f'/song_page/{song.id}/')
        self.assertIsInstance(response.context['form'], SketchForm)
        self.assertContains(response, 'name="text"')

    def test_uses_songs_list_template(self):
        """ test: uses list template """
        song = Song.objects.create(name="Test song")
        response = self.client.get(f'/song_page/{song.id}/')
        self.assertTemplateUsed(response, 'song_page.html')

    def test_displays_all_items_from_model(self):
        """ test: all elements a shown """
        correct_song = Song.objects.create(name="Test song")

        Sketch.objects.create(text='item 1', song=correct_song)
        Sketch.objects.create(text='item 2', song=correct_song)

        other_song = Song.objects.create(name="Other song")
        
        Sketch.objects.create(text='other song item 1', song=other_song)
        Sketch.objects.create(text='other song item 2', song=other_song)

        response = self.client.get(f'/song_page/{correct_song.id}/')

        self.assertContains(response, 'item 1')
        self.assertContains(response, 'item 2')
        self.assertNotContains(response, 'other song item 1')
        self.assertNotContains(response, 'other song item 2')

    def test_passes_correct_song_to_template(self):
        other_song = Song.objects.create(name='other song')
        correct_song = Song.objects.create(name='correct song')
        response = self.client.get(f'/song_page/{correct_song.id}/')
        self.assertEqual(response.context['song'], correct_song)

    
    def test_can_redirect_after_the_POST(self):
        response = self.client.post('/song_page/new', data={'name': 'A new list item'})
        new_song = Song.objects.first()
        self.assertRedirects(response, f'/song_page/{new_song.id}/')

    def test_can_save_a_POST_request_to_existing_song(self):
        other_song = Song.objects.create(name='Other song')
        correct_song = Song.objects.create(name='Correct Song')
        self.client.post(
                    f'/song_page/{correct_song.id}/',
                    data={'text': 'A new chunk to existing song', "song": correct_song.id})
            
        self.assertEqual(Sketch.objects.count(), 1)
        new_item = Sketch.objects.first()
        self.assertEqual(new_item.text, 'A new chunk to existing song')
        self.assertEqual(new_item.song, correct_song)


    def test_invalid_input_renders_home_page(self):
        response = self.post_ivalid_song_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'homepage.html')
    

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.post_ivalid_song_input()
        self.assertContains(response, escape(EMPTY__ITEM_ERROR))


    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_ivalid_song_input()
        self.assertIsInstance(response.context['form'], SongForm)


    def test_invalid_song_item_arent_saved_in_db(self):
        self.post_invalid_chunk_input()
        self.assertEqual(Sketch.objects.count(), 0)


    def test_for_invalid_input_renders_template(self):
        response = self.post_invalid_chunk_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'song_page.html')

    def test_for_invalid_chunk_input_passes_from_to_template(self):
        response = self.post_invalid_chunk_input()
        self.assertIsInstance(response.context['form'], SketchForm)

    def test_that_validation_error_on_invalid_chunk_shows_error_on_page(self):
        response = self.post_invalid_chunk_input()
        self.assertContains(response, escape(EMPTY__ITEM_ERROR))


class MySongsTest(TestCase):

    def test_my_songs_url_renders_my_songs_template(self):
        User.objects.create(email='a@b.com')
        response = self.client.get('/songs/users/a@b.com')
        self.assertTemplateUsed(response, 'my_songs.html')

    def test_passes_correct_owner_to_template(self):
        User.objects.create(email='whorg@owner.com')
        correct_user = User.objects.create(email='a@b.com')
        response = self.client.get('/songs/users/a@b.com')
        self.assertEqual(response.context['owner'], correct_user)

    def test_song_owner_is_saved_if_user_is_authenticated(self):
        user = User.objects.create(email='a@b.com')
        self.client.force_login(user)
        self.client.post('/song_page/new', data={'name': 'new_song'})
        song = Song.objects.first()
        self.assertEqual(song.owner, user)


@patch('pocket_chords.views.NewSongForm')
class NewSongViewIntegratedTest(TestCase):

    def setUp(self) -> None:
        self.request = HttpRequest()
        self.request.POST['name'] = 'new song name'
        self.request.user = Mock()

    @patch('pocket_chords.views.redirect')
    def test_passes_POST_data_to_NewSongForm(self, mock_redirect, mockNewSongForm):
        new_song2(self.request)
        mockNewSongForm.assert_called_once_with(data=self.request.POST)

    @patch('pocket_chords.views.redirect')
    def test_song_owner_is_saved_if_user_is_authenticated(self,mock_redirect ,mockNewSongForm):
        mock_form = mockNewSongForm.return_value
        mock_form.is_valid.return_value = True
        new_song2(self.request)
        mock_form.save.assert_called_once_with(owner=self.request.user)

    @patch('pocket_chords.views.redirect')
    def test_redirect_to_form_returned_object_if_form_is_valid(
        self, mock_redirect, mockNewSongForm
    ):
        mock_form = mockNewSongForm.return_value
        mock_form.is_valid.return_value = True

        response = new_song2(self.request)

        self.assertEqual(response, mock_redirect.return_value)
        mock_redirect.assert_called_once_with(mock_form.save.return_value)

    @patch('pocket_chords.views.render')
    def test_renders_home_template_with_form_if_form_invalid(
        self, mock_render, mockNewSongForm
        ):
            mock_form = mockNewSongForm.return_value
            mock_form.is_valid.return_value = False
            response = new_song2(self.request)
            self.assertEqual(response, mock_render.return_value)
            mock_render.assert_called_once_with(
            self.request, 'home.html', {'form': mock_form}
            )