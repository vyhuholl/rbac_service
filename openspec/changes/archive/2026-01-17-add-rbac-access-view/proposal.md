# Change: Add Access View

## Why
The RBAC system currently provides models for roles, business elements, and access rules, but lacks API endpoints for checking user access to resources. An access view is needed to enable applications to verify if a user has the required permissions for a specific resource, which is a core functionality of any RBAC implementation.

## What Changes
- Add a new API endpoint `/api/rbac/access/` that accepts user ID, resource name, and permissions
- Implement access checking logic using the existing RBAC models (Role, BusinessElement, AccessRoleRule)
- Return the resource data if access is granted, or appropriate HTTP error codes (401/403) if denied
- Use Django REST Framework for the view implementation

## Impact
- Affected specs: rbac (adding new requirement for access view)
- Affected code: rbac/views.py, rbac/urls.py, rbac_service/urls.py
- No breaking changes to existing functionality