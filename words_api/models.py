from django.db import models
from user_api.models import User
from category_api.models import Category


class Word(models.Model):
    id = models.AutoField(
        verbose_name='ID',
        primary_key=True
    )

    enValue = models.CharField(
        verbose_name='Слово (англ)',
        blank=False, 
        null=False,
        default=''
    )

    ruValue = models.CharField(
        verbose_name='Слово (рус)',
        blank=False, 
        null=False,
        default=''
    )

    audioLink = models.CharField(
        verbose_name='Аудиозапись',
        blank=False,
        null=True
    )

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"

    def __str__(self) -> str:
        return self.enValue


class UserWord(models.Model):
    id = models.AutoField(
        verbose_name='ID',
        primary_key=True
    )

    word = models.ForeignKey(
        Word,
        verbose_name='Слово',
        blank=False, 
        null=False,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    frequency = models.IntegerField(
        verbose_name='Частотность',
        blank=False, 
        null=False,
        default=0
    )

    isChecked = models.BooleanField(
        verbose_name='',
        default=False
    )

    class Meta:
        verbose_name = "Слово (пользователя)"
        verbose_name_plural = "Слова (пользователя)"

    def __str__(self) -> str:
        return f'{self.id} | {self.word.enValue} | {self.user.name}'
