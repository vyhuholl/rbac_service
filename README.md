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

## RBAC API Views

The RBAC service provides REST API endpoints for access control management and administration.

### Access Check View
The access check endpoint allows applications to verify if a user has the required permissions for a specific resource.

**Endpoint**: `GET /api/rbac/access/`

**Query Parameters**:
- `user_id`: UUID of the user
- `resource`: Name of the business element/resource
- `permissions`: Comma-separated list of required permissions (e.g., "read", "read,create")

**Response Codes**:
- `200 OK`: User has required permissions, returns resource data
- `401 Unauthorized`: User not found or inactive
- `403 Forbidden`: User lacks required permissions or resource doesn't exist

**Example**:
```bash
GET /api/rbac/access/?user_id=123e4567-e89b-12d3-a456-426614174000&resource=Document&permissions=read
```

### Admin Management Views
Superusers can manage RBAC rules programmatically through REST API endpoints. These endpoints require superuser authentication.

#### Role Management
**Endpoints**:
- `GET /api/rbac/roles/` - List all roles
- `POST /api/rbac/roles/` - Create a new role
- `GET /api/rbac/roles/{id}/` - Retrieve a specific role
- `PUT /api/rbac/roles/{id}/` - Update a role
- `PATCH /api/rbac/roles/{id}/` - Partially update a role
- `DELETE /api/rbac/roles/{id}/` - Delete a role

**Request/Response Format**:
```json
{
  "id": "uuid",
  "name": "RoleName",
  "description": "Optional description",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Business Element Management
**Endpoints**:
- `GET /api/rbac/business-elements/` - List all business elements
- `POST /api/rbac/business-elements/` - Create a new business element
- `GET /api/rbac/business-elements/{id}/` - Retrieve a specific business element
- `PUT /api/rbac/business-elements/{id}/` - Update a business element
- `PATCH /api/rbac/business-elements/{id}/` - Partially update a business element
- `DELETE /api/rbac/business-elements/{id}/` - Delete a business element

**Request/Response Format**:
```json
{
  "id": "uuid",
  "name": "ElementName",
  "description": "Optional description",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

#### Access Rule Management
**Endpoints**:
- `GET /api/rbac/access-rules/` - List all access rules
- `POST /api/rbac/access-rules/` - Create a new access rule
- `GET /api/rbac/access-rules/{id}/` - Retrieve a specific access rule
- `PUT /api/rbac/access-rules/{id}/` - Update an access rule
- `PATCH /api/rbac/access-rules/{id}/` - Partially update an access rule
- `DELETE /api/rbac/access-rules/{id}/` - Delete an access rule

**Request/Response Format**:
```json
{
  "id": "uuid",
  "role": "role-uuid",
  "element": "element-uuid",
  "read_permission": true,
  "read_all_permission": false,
  "create_permission": true,
  "update_permission": false,
  "update_all_permission": false,
  "delete_permission": true,
  "delete_all_permission": false
}
```

### Authentication and Authorization
All admin management endpoints require:
- **Authentication**: Valid user session or token
- **Authorization**: User must have `is_superuser=True`

Unauthorized requests return:
- `401 Unauthorized` for unauthenticated requests
- `403 Forbidden` for authenticated but non-superuser requests

### Validation and Constraints
- Role names must be unique
- Business element names must be unique
- Each (role, element) combination can have only one access rule
- Attempting to create duplicate access rules returns `400 Bad Request`
