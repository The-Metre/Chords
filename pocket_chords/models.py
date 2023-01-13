from django.db import models

# Create your models here.

class Song(models.Model):
    """ Contain info about a song """
    name = models.CharField(max_length=255)
    text = models.TextField(default='')

class Sketch(models.Model):
    """ Class contain string('notes')
        Example in physical world: stickers
        in a book
    """
    pass