from django.db import models
import uuid
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(primary_key=True, unique=True)
    username = models.CharField(max_length=30, unique=True, default='')
    REQUIRED_FIELDS = ['username']
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

    def __str__(self):
        return self.email
