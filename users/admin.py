from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom admin for User model."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Личная информация'),
            {'fields': ('first_name', 'middle_name', 'last_name')},
        ),
        (
            _('Права'),
            {
                'fields': ('is_active', 'is_staff', 'is_superuser'),
            },
        ),
        (_('Важные даты'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'middle_name',
                    'last_name',
                    'password1',
                    'password2',
                ),
            },
        ),
    )
    list_display = (
        'email',
        'first_name',
        'middle_name',
        'last_name',
        'is_staff',
        'is_active',
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'middle_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()
