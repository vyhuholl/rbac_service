from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser):
    """Custom user model with email as username field."""

    email = models.EmailField(
        'E-mail',
        unique=True,
        max_length=255,
    )
    first_name = models.CharField('Имя', max_length=255)
    middle_name = models.CharField(
        'Отчество',
        max_length=255,
        blank=True,
    )
    last_name = models.CharField('Фамилия', max_length=255)
    is_active = models.BooleanField('Активен', default=True)
    is_staff = models.BooleanField('Сотрудник', default=False)
    is_superuser = models.BooleanField('Суперпользователь', default=False)
    date_joined = models.DateTimeField('Дата создания', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

    def has_perm(self, perm, obj=None):
        """Return True if user has the given permission."""
        return self.is_superuser

    def has_perms(self, perm_list, obj=None):
        """Return True if user has each of the specified permissions."""
        return self.is_superuser

    def has_module_perms(self, app_label):
        """Return True if user has permissions to view the app."""
        return self.is_superuser
