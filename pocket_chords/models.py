from django.db import models
from django.urls import reverse

from django.conf import settings
from django.db.models import CheckConstraint, Q

# Create your models here.

MUSIC_NOTES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']


class MusicNote(models.Model):
    """ Contain information of notes in chords
    """
    name = models.CharField(max_length=2, blank=False, unique=True)
    
    class Meta:
        constraints = [
            CheckConstraint(
                check = Q(name__in=MUSIC_NOTES),
                name = 'check_music_note_name',
            ),
        ]

class Chord(models.Model):
    """ Contain information of specific chord
    """
    name = models.CharField(max_length=30, blank=False, unique=True)
    root_note = models.ForeignKey(MusicNote, on_delete=models.CASCADE)

class ChordNotesRelation(models.Model):
    """ Contain relations between chords and notes models """
    chord_name = models.ForeignKey(Chord, on_delete=models.CASCADE)
    chord_note = models.ForeignKey(MusicNote, on_delete=models.CASCADE)

    class Meta:
        ordering = ('chord_name', )
        unique_together = (('chord_name', 'chord_note'), )


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




