# Generated by Django 5.0.4 on 2024-04-09 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('words_api', '0003_remove_word_value_userword_frequency_word_en_value_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='word',
            old_name='audio',
            new_name='audioLink',
        ),
        migrations.RenameField(
            model_name='word',
            old_name='en_value',
            new_name='enValue',
        ),
        migrations.RenameField(
            model_name='word',
            old_name='ru_value',
            new_name='ruValue',
        ),
    ]
