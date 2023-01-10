from django.db import models

# Create your models here.

class Song(models.Model):
    name = models.CharField(default='unknows', max_length=255)
    text = models.TextField(default='')