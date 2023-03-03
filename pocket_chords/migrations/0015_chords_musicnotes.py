# Generated by Django 3.2.12 on 2023-03-03 19:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pocket_chords', '0014_song_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='MusicNotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, unique=True)),
                ('chord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pocket_chords.chords')),
            ],
        ),
    ]
