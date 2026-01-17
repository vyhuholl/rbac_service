from rest_framework import permissions


class IsSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow superusers to access the view.
    """

    def has_permission(self, request, view):
        """
        Return True if user is a superuser, False otherwise.
        """
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        )
