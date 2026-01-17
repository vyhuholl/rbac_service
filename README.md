# rbac_service
Role-Based Access Control service.

## API Schemas
- OpenAPI – available at `api/schema/`
- Swagger – available at `api/schema/swagger-ui/`
- ReDoc – available at `api/schema/redoc/`

## Custom User Model

This project uses a custom user model (`users.User`) that extends Django's `AbstractBaseUser`. The custom user model includes:

- **Email**: Used as the unique username field for authentication
- **First Name**: User's first name (required)
- **Middle Name**: User's middle name (optional)
- **Last Name**: User's last name (required)
- **Standard Django fields**: `is_active`, `is_staff`, `is_superuser`, `date_joined`

### Important Configuration

The `AUTH_USER_MODEL` setting in `rbac_service/settings.py` is configured to use the custom user model:

```python
AUTH_USER_MODEL = 'users.User'
```

### User Management

Users can be created and managed through:
- Django Admin interface at `/admin/`
- API at `/user/api/register`, `/user/api/login`, `/user/api/logout`, `/user/api/update` and `/user/api/delete`
- Programmatically using `User.objects.create_user()` and `User.objects.create_superuser()`

### Authentication

Authentication uses email as the username field. Login credentials are:
- **Username**: User's email address
- **Password**: User's password

## RBAC Models

This project implements core Role-Based Access Control (RBAC) functionality with the following models:

### Role Model (`rbac.Role`)
Represents user roles in the system:
- **Name**: Unique role identifier
- **Description**: Optional description of the role's purpose
- **Timestamps**: Automatic `created_at` and `updated_at` fields

### Business Element Model (`rbac.BusinessElement`)
Represents resources or objects that can have access controls:
- **Name**: Unique resource identifier
- **Description**: Optional description of the resource
- **Timestamps**: Automatic `created_at` and `updated_at` fields

### Access Role Rule Model (`rbac.AccessRoleRule`)
Defines permissions for a role on a specific business element:
- **Role**: Foreign key to the Role model
- **Element**: Foreign key to the BusinessElement model
- **Permissions**: Boolean fields for granular access control:
  - `read_permission`: Read access to own resources
  - `read_all_permission`: Read access to all resources
  - `create_permission`: Create new resources
  - `update_permission`: Update access to own resources
  - `update_all_permission`: Update access to all resources
  - `delete_permission`: Delete access to own resources
  - `delete_all_permission`: Delete access to all resources

### Unique Constraints
- Role names must be unique
- Business element names must be unique
- Each (role, element) combination can have only one access rule

### Django Admin Integration
All RBAC models are registered with Django's admin interface for easy management at `/admin/rbac/`.
