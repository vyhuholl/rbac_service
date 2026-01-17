from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'password_confirm',
            'first_name',
            'middle_name',
            'last_name',
        )

    def validate_email(self, value):
        """Check that email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _('A user with this email already exists.')
            )
        return value

    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {
                    'password_confirm': _(
                        'Password confirmation does not match.'
                    )
                }
            )
        return attrs

    def create(self, validated_data):
        """Create user with validated data."""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        """Validate credentials and authenticate user."""
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    _('Invalid email or password.')
                )
            if not user.is_active:
                raise serializers.ValidationError(
                    _('User account is disabled.')
                )
            attrs['user'] = user
        else:
            raise serializers.ValidationError(
                _('Must include email and password.')
            )

        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile information."""

    class Meta:
        model = User
        fields = ('first_name', 'middle_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': False},
            'middle_name': {'required': False},
            'last_name': {'required': False},
        }
