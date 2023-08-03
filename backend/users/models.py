from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',
        help_text='Введите электронную почту'
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Введите имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Введите фамилию'
    )
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль',
        help_text='Введите пароль'
    )

    class Meta:
        verbose_name = 'Пользователь'


class UserFollow(models.Model):
    user = models.ForeignKey(
        User,
        related_name='follower',
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        help_text='Укажите подписчика'
    )
    author = models.ForeignKey(
        User,
        related_name='following',
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Укажите автора'
    )

    class Meta:
        verbose_name = 'Подписки'
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_user_author'
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')),
                name='same_user_follow'
            ),
        ]
