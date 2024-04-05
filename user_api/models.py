from django.db import models


class User(models.Model):
    id = models.AutoField(
        verbose_name='ID',
        primary_key=True
    )
    
    name = models.CharField(
        max_length=128, 
        verbose_name='Имя',
        blank=False, 
        null=False
    )

    email = models.EmailField(
        unique=True, 
        verbose_name='Почта',
        blank=False, 
        null=False
    )

    password = models.CharField(
        verbose_name='Пароль',
        blank=True, 
        null=True
    )

    is_active = models.BooleanField(
        verbose_name='Активность',
        default=True
    )

    created_at = models.DateTimeField(
        verbose_name='Дата регистрации',
        auto_now_add=True
    )

    def __str__(self) -> str:
        return f'ID: {self.id} | {self.name}, {self.email}'
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
