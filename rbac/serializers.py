from rest_framework import serializers
from .models import BusinessElement, Role, AccessRoleRule


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model."""

    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class BusinessElementSerializer(serializers.ModelSerializer):
    """Serializer for BusinessElement model."""

    class Meta:
        model = BusinessElement
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']


class AccessRoleRuleSerializer(serializers.ModelSerializer):
    """Serializer for AccessRoleRule model."""

    class Meta:
        model = AccessRoleRule
        fields = [
            'id',
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
