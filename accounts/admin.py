from django.contrib import admin
from .models import Token, ChordsUser, ChordsUserManager
# Register your models here.


admin.site.register(Token)
admin.site.register(ChordsUser)