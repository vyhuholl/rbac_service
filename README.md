# rbac_service
Role-Based Access Control service.

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

**⚠️ Breaking Change**: This setting must be configured before creating any migrations. If migrations already exist, they will need to be reset before implementing this custom user model.

### User Management

Users can be created and managed through:
- Django Admin interface at `/admin/`
- Programmatically using `User.objects.create_user()` and `User.objects.create_superuser()`

### Authentication

Authentication uses email as the username field. Login credentials are:
- **Username**: User's email address
- **Password**: User's password
