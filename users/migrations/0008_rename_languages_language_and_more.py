# Generated by Django 5.1.5 on 2025-02-11 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_languages_remove_profile_cooking_goals_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Languages',
            new_name='Language',
        ),
        migrations.RenameModel(
            old_name='ProfileLanguages',
            new_name='ProfileLanguage',
        ),
    ]
