from django.contrib import admin

from .models import AccessRoleRule, BusinessElement, Role, UserRole


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(AccessRoleRule)
class AccessRoleRuleAdmin(admin.ModelAdmin):
    list_display = [
        'role',
        'element',
        'read_permission',
        'read_all_permission',
        'create_permission',
        'update_permission',
        'update_all_permission',
        'delete_permission',
        'delete_all_permission',
    ]
    list_filter = ['role', 'element']


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = [
        'user__email',
        'user__first_name',
        'user__last_name',
        'role__name',
    ]
