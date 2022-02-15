from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    group = [('user', 'user'), ('moderator', 'moderator'), ('admin', 'admin')]
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль',
        blank=True,
        choices=group
    )
