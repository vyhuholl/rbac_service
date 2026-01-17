# Change: Add Custom User Model

## Why
The default Django User model does not meet the RBAC service requirements for user identity management. A custom user model is needed to store first name, middle name, last name, and use email as the username field for authentication and authorization purposes.

## What Changes
- Create a custom User model extending AbstractBaseUser with first_name, middle_name, last_name, and email fields
- Configure email as the unique username field for authentication
- Update Django settings to use the custom user model (AUTH_USER_MODEL)
- Create user management migrations

**BREAKING**: This change requires setting AUTH_USER_MODEL before any migrations are created. If migrations already exist, they will need to be reset.

## Impact
- Affected specs: New capability `user-auth`
- Affected code: [`rbac_service/settings.py`](rbac_service/settings.py), new user app/models
- Dependencies: Requires database migration; must be done before any other models reference the User model
