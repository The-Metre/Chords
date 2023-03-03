from django.db import models
from django.urls import reverse

from django.conf import settings

# Create your models here.

class Chords(models.Model):
    """ Contain information of specific chord
    """
    name = models.CharField(max_length=30, blank=False, unique=True)
    root_note = models.CharField(max_length=5, default='')

class ChordNote(models.Model):
    """ Contain information of notes in chords
    """
    name = models.CharField(max_length=10, blank=False)
    chord = models.ForeignKey(Chords, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('name', 'chord'), )

class Song(models.Model):
    """ Contain info about a song """
    name = models.CharField(max_length=255, blank=False, unique=True)
    text = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        """ Get an absolute url """
        return reverse('song_page', args=[self.id])
    
    def create_new(self):
        pass


class Sketch(models.Model):
    """ Class contain string('notes')
        Example in physical world: stickers
        in a book
    """
    text = models.TextField(max_length=255, blank=False)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
    
    def __str__(self):
        return self.text
