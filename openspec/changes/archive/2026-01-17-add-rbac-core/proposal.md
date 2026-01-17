# Change: Add Core RBAC Functionality

## Why
The RBAC service requires core role-based access control functionality to manage user roles, business elements, and access rules. This is the foundational capability for the entire RBAC system, enabling fine-grained authorization control over protected resources.

## What Changes
- Create a new Django app `rbac` for RBAC functionality
- Create `Role` model to describe user roles
- Create `BusinessElement` model to describe objects to manage access to
- Create `AccessRoleRule` model to describe access rules for a particular role to a particular element
- Add `AccessRoleRule` permission fields: read_permission, read_all_permission, create_permission, update_permission, update_all_permission, delete_permission, delete_all_permission (all boolean)
- Register models with Django admin for management
- Create database migrations for the new models

## Impact
- Affected specs: New capability `rbac`
- Affected code: [`rbac_service/settings.py`](rbac_service/settings.py) (add rbac to INSTALLED_APPS), new rbac app
- Dependencies: Requires database migration
