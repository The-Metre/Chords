from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class ChordsUserManager(BaseUserManager):
    """ manager of the Chords proj user """

    def create_user(self, email):
        """ create a user """
        ChordsUser.objects.create(email=email)

    def create_superuser(self, email, password):
        """ create superuser """
        self.create_user(email)


class ChordsUser(AbstractBaseUser, PermissionsMixin):
    """ user of pocket chords """
    email = models.EmailField(primary_key=True)
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email', 'height']

    object = ChordsUserManager()

    @property
    def is_staff(self):
        return self.email == 'harry.percival.example.com'

    @property
    def is_active(self):
        return True



class Token(models.Model):
    """ marker """
    email = models.EmailField()
    uid = models.CharField(max_length=255)