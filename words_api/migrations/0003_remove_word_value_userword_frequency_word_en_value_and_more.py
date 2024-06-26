# Generated by Django 5.0.4 on 2024-04-07 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('words_api', '0002_alter_word_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='value',
        ),
        migrations.AddField(
            model_name='userword',
            name='frequency',
            field=models.IntegerField(default=0, verbose_name='Частотность'),
        ),
        migrations.AddField(
            model_name='word',
            name='en_value',
            field=models.CharField(default='', verbose_name='Слово (англ)'),
        ),
        migrations.AddField(
            model_name='word',
            name='ru_value',
            field=models.CharField(default='', verbose_name='Слово (рус)'),
        ),
    ]
