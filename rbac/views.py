from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .models import BusinessElement, UserRole, AccessRoleRule
from .serializers import BusinessElementSerializer

User = get_user_model()


class AccessView(APIView):
    """View for checking user access to business resources."""

    def get(self, request):
        user_id = request.query_params.get('user_id')
        resource_name = request.query_params.get('resource')
        permissions_str = request.query_params.get('permissions', '')

        if not user_id or not resource_name or not permissions_str:
            return Response(
                {
                    'error': 'Missing required parameters: user_id, resource, permissions'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate user exists
        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found or inactive'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Get business element
        try:
            business_element = BusinessElement.objects.get(name=resource_name)
        except BusinessElement.DoesNotExist:
            return Response(
                {'error': 'Resource not found'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Parse permissions
        required_permissions = [
            p.strip() for p in permissions_str.split(',') if p.strip()
        ]

        # Get user's roles
        user_roles = UserRole.objects.filter(user=user).values_list(
            'role', flat=True
        )

        # Check if any user role has all required permissions for this element
        has_access = False
        for role_id in user_roles:
            try:
                rule = AccessRoleRule.objects.get(
                    role_id=role_id, element=business_element
                )
                if all(
                    getattr(rule, perm + '_permission', False)
                    for perm in required_permissions
                ):
                    has_access = True
                    break
            except AccessRoleRule.DoesNotExist:
                continue

        if not has_access:
            return Response(
                {'error': 'Insufficient permissions'},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Return resource data
        serializer = BusinessElementSerializer(business_element)
        return Response(serializer.data)
