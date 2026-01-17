from rest_framework import serializers
from .models import BusinessElement


class BusinessElementSerializer(serializers.ModelSerializer):
    """Serializer for BusinessElement model."""

    class Meta:
        model = BusinessElement
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
