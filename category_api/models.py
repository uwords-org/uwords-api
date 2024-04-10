from django.db import models

# Create your models here.

class Category(models.Model):
    id = models.AutoField(
        verbose_name='ID',
        primary_key=True
    )

    title = models.CharField(
        verbose_name='Название категории',
        blank=False, 
        null=False,
        default=''
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.title


class CatWord(models.Model):
    id = models.AutoField(
        verbose_name='ID',
        primary_key=True
    )

    ruValue = models.CharField(
        verbose_name='Слово (на рус)',
        blank=False, 
        null=False,
        default=''
    )

    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Слово категорическое"
        verbose_name_plural = "Слова категорические"

    def __str__(self) -> str:
        return f'{self.ruValue} | {self.category.title}'