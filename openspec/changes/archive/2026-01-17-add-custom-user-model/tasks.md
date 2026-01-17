## 1. Project Setup

- [x] 1.1 Create new Django app `users` using `uv run manage.py startapp users`
- [x] 1.2 Add `users` to INSTALLED_APPS in [`rbac_service/settings.py`](rbac_service/settings.py)
- [x] 1.3 Set AUTH_USER_MODEL = 'users.User' in [`rbac_service/settings.py`](rbac_service/settings.py)

## 2. User Model Implementation

- [x] 2.1 Create custom UserManager in `users/managers.py` with create_user() and create_superuser() methods
- [x] 2.2 Create custom User model in `users/models.py` extending AbstractBaseUser
- [x] 2.3 Add email field as CharField with unique=True, max_length=255
- [x] 2.4 Add first_name field as CharField with max_length=255
- [x] 2.5 Add middle_name field as CharField with max_length=255 (optional)
- [x] 2.6 Add last_name field as CharField with max_length=255
- [x] 2.7 Add is_active, is_staff, is_superuser boolean fields with appropriate defaults
- [x] 2.8 Add date_joined DateTimeField with auto_now_add=True
- [x] 2.9 Set USERNAME_FIELD = 'email' on the User model
- [x] 2.10 Configure REQUIRED_FIELDS as empty list

## 3. Django Admin Integration

- [x] 3.1 Create custom UserAdmin class in `users/admin.py`
- [x] 3.2 Register the User model with the custom UserAdmin
- [x] 3.3 Configure admin display for email, first_name, middle_name, last_name
- [x] 3.4 Configure admin filters for is_active and is_staff

## 4. Database Migration

- [x] 4.1 Create initial migrations for the users app: `uv run manage.py makemigrations users`
- [x] 4.2 Run migrations: `uv run manage.py migrate`
- [x] 4.3 Verify the users_user table is created in the database

## 5. Testing

- [x] 5.1 Write unit tests for UserManager.create_user()
- [x] 5.2 Write unit tests for UserManager.create_superuser()
- [x] 5.3 Write unit tests for User model field validation
- [x] 5.4 Write unit tests for email uniqueness constraint
- [x] 5.5 Write integration tests for Django admin user creation
- [x] 5.6 Run all tests with pytest: `pytest`
- [x] 5.7 Verify code coverage meets 80% threshold

## 6. Documentation

- [x] 6.1 Add docstrings to UserManager methods
- [x] 6.2 Add docstrings to User model
- [x] 6.3 Update README.md with custom user model information
- [x] 6.4 Document the AUTH_USER_MODEL setting requirement

## 7. Validation

- [x] 7.1 Verify Django admin can create users
- [x] 7.2 Verify Django admin can modify users
- [x] 7.3 Verify Django admin can delete users
- [x] 7.4 Verify authentication works with email and password
- [x] 7.5 Run `ruff check` for linting
- [x] 7.6 Run `ruff format` for code formatting
