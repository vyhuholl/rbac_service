# Change: Add RBAC Admin Views

## Why
The RBAC system currently provides models for roles, business elements, and access rules, and an access check endpoint. However, there is no API interface for superusers to manage these RBAC rules programmatically. Superusers need REST API endpoints to create, read, update, and delete roles, business elements, and access rules without relying on the Django admin interface.

## What Changes
- Add serializers for Role, BusinessElement, and AccessRoleRule models
- Add ViewSets for CRUD operations on Role, BusinessElement, and AccessRoleRule
- Create custom permission class to restrict access to superusers only
- Add URL configuration for the new admin endpoints
- Use Django REST Framework for all view implementations

## Impact
- Affected specs: rbac (adding new requirements for admin views)
- Affected code: rbac/serializers.py, rbac/views.py, rbac/urls.py, rbac_service/urls.py
- No breaking changes to existing functionality
