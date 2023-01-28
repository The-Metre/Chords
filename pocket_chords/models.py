from django.db import models
from django.urls import reverse


# Create your models here.

class Song(models.Model):
    """ Contain info about a song """
    name = models.CharField(max_length=255, blank=False, unique=True)
    text = models.TextField(blank=True)

    def get_absolute_url(self):
        """ Get an absolute url """
        return reverse('song_page', args=[self.id])


class Sketch(models.Model):
    """ Class contain string('notes')
        Example in physical world: stickers
        in a book
    """
    text = models.TextField(max_length=255, blank=False)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
        unique_together = ('text', 'song')
    
    def __str__(self):
        return self.text
