from django.db import models
from user_api.models import User


class Word(models.Model):
    id = models.AutoField(
        verbose_name='ID',
        primary_key=True
    )

    value = models.CharField(
        verbose_name='Слово',
        blank=False, 
        null=False,
        unique=True
    )

    audio = models.CharField(
        verbose_name='Аудиозапись',
        blank=False,
        null=False
    )

    class Meta:
        verbose_name = "Слово"
        verbose_name_plural = "Слова"

    def __str__(self) -> str:
        return self.value


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

    isChecked = models.BooleanField(
        verbose_name='',
        default=False
    )
