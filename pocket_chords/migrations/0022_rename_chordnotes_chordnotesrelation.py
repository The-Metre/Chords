# Generated by Django 3.2.12 on 2023-03-07 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pocket_chords', '0021_chordnotes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChordNotes',
            new_name='ChordNotesRelation',
        ),
    ]
