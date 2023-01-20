from django.db import models

# Create your models here.

class Song(models.Model):
    """ Contain info about a song """
    name = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=True)

class Sketch(models.Model):
    """ Class contain string('notes')
        Example in physical world: stickers
        in a book
    """
    text = models.TextField(max_length=255, blank=False)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
