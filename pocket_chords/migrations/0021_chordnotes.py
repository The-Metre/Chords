# Generated by Django 3.2.12 on 2023-03-04 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pocket_chords', '0020_rename_chords_chord'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChordNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chord_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pocket_chords.chord')),
                ('chord_note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pocket_chords.musicnote')),
            ],
            options={
                'ordering': ('chord_name',),
                'unique_together': {('chord_name', 'chord_note')},
            },
        ),
    ]
