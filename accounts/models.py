from django.contrib import auth
from django.db import models
import uuid
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128, default='')
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True


class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(default = uuid.uuid4,max_length=40)

