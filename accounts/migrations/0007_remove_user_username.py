# Generated by Django 3.2.12 on 2023-03-22 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
