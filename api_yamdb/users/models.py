from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = [
        ('admin', ADMIN),
        ('moderator', MODERATOR),
        ('user', USER),
    ]

    username = models.CharField(
        max_length=100,
        unique=True,
        null=False,
    )
    email = models.EmailField(
        max_length=250,
        unique=True,
    )
    bio = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Биография',
    )
    confirmation_code = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Код подтверждения',
    )
    role = models.CharField(
        max_length=50,
        default=USER,
        choices=ROLE_CHOICES,
        verbose_name='Роль',
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
    )

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'username',),
                name='unique_auth'
            ),
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
