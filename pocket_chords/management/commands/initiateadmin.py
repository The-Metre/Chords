from typing import Any
from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import User

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        if User.objects.count() == 0:
            for user in settings.ADMINS:
                username = 'admin'
                email = 'admin@gmail.com'
                password = 'admin'
                print(f'Createting account for {username} {email}')
                admin = User.objects.create_superuser(email=email, password=password, username=username)
                admin.is_active = True
                admin.is_admin = True
                admin.save()
        else:
            print('Admin accounts can only be initialized if no Users exist')