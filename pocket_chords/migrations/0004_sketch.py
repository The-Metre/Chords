# Generated by Django 3.2.12 on 2023-01-13 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pocket_chords', '0003_alter_song_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sketch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]