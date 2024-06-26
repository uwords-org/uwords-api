# Generated by Django 5.0.4 on 2024-04-10 15:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='CatWord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('ruValue', models.CharField(default='', verbose_name='Слово (на рус)')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category_api.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Слово категорическое',
                'verbose_name_plural': 'Слова категорические',
            },
        ),
    ]
