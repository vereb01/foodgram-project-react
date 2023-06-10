from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    """Модель пользователей"""
    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        max_length=254,
        help_text='Введите адрес электронной почты'
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        validators=(validate_username,),
        unique=True,
        help_text='Будет показано'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ('pk',)
        verbose_name = 'пользователя'
        verbose_name_plural = 'пользователи'
        constraints = (
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_auth'
            ),
        )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Subscription(models.Model):
    """Модель для подписок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор рецепта',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'user'],
                name='unique_subscribe'
            )
        ]
