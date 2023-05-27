from django.db import models
import uuid
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


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
