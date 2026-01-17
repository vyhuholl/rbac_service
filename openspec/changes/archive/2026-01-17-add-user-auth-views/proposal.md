# Change: Add User Authentication Views

## Why
The RBAC service currently has a custom User model but lacks API endpoints for user authentication and management. To enable user-facing functionality, we need Django REST Framework views for registration, login, logout, account deletion, and user profile updates.

## What Changes
- Create DRF serializers for user registration and profile updates
- Implement Register view for new user creation
- Implement Login view for user authentication
- Implement Logout view for user session termination
- Implement Account Deletion view (soft-delete: set is_active to False)
- Implement User Info Update view for profile modifications
- Create URL routing for user authentication endpoints
- Add authentication classes and permission configurations

## Impact
- Affected specs: `user-auth` capability (extending existing spec)
- Affected code: [`users/views.py`](users/views.py), new `users/serializers.py`, new `users/urls.py`, [`rbac_service/urls.py`](rbac_service/urls.py)
- Dependencies: Requires Django REST Framework (already in project)
