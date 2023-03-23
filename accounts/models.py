from django.contrib import auth
from django.db import models
import uuid
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True, unique=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_anonymous = False
    is_authenticated = True

    objects = UserManager()


    def __str__(self):
        return self.email

class Token(models.Model):
    email = models.EmailField()
    uid = models.CharField(default = uuid.uuid4,max_length=40)

