# Generated by Django 3.2.12 on 2023-01-10 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pocket_chords', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='name',
            field=models.CharField(default='unknows', max_length=255),
        ),
        migrations.AddField(
            model_name='song',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
