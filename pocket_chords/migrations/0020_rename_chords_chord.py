# Generated by Django 3.2.12 on 2023-03-04 09:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pocket_chords', '0019_alter_chords_root_note'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Chords',
            new_name='Chord',
        ),
    ]
