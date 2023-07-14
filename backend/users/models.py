from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)

    class Meta:
        ordering = ['id']


class UserFollow(models.Model):
    user = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_user_author'
            )
        ]
