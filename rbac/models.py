from django.db import models
import uuid


class Role(models.Model):
    """Role model for RBAC system.

    Represents a user role that can be assigned permissions for various
    business elements in the system.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', unique=True, max_length=255)
    description = models.CharField(
        'Описание',
        max_length=1000,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class BusinessElement(models.Model):
    """Business element model for RBAC system.

    Represents a resource or object in the system that can have access
    controls applied to it through roles and permissions.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Название', unique=True, max_length=255)
    description = models.CharField(
        'Описание',
        max_length=1000,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Бизнес-элемент'
        verbose_name_plural = 'Бизнес-элементы'

    def __str__(self):
        return self.name


class AccessRoleRule(models.Model):
    """Access rule model defining permissions for a role on a business element.

    Defines the specific permissions that a role has for a particular
    business element, including granular permissions like read, create,
    update, and delete with additional "all" variants for ownership-based access.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        verbose_name='Роль',
    )
    element = models.ForeignKey(
        BusinessElement,
        on_delete=models.CASCADE,
        verbose_name='Бизнес-элемент',
    )
    read_permission = models.BooleanField('Чтение (свои)', default=False)
    read_all_permission = models.BooleanField('Чтение (все)', default=False)
    create_permission = models.BooleanField('Создание', default=False)
    update_permission = models.BooleanField('Обновление (свои)', default=False)
    update_all_permission = models.BooleanField(
        'Обновление (все)', default=False
    )
    delete_permission = models.BooleanField('Удаление (свои)', default=False)
    delete_all_permission = models.BooleanField(
        'Удаление (все)', default=False
    )

    class Meta:
        unique_together = ('role', 'element')
        verbose_name = 'Правило доступа'
        verbose_name_plural = 'Правила доступа'

    def __str__(self):
        return f'{self.role.name} - {self.element.name}'
