## 1. Project Setup

- [ ] 1.1 Create new Django app `users` using `uv run manage.py startapp users`
- [ ] 1.2 Add `users` to INSTALLED_APPS in [`rbac_service/settings.py`](rbac_service/settings.py)
- [ ] 1.3 Set AUTH_USER_MODEL = 'users.User' in [`rbac_service/settings.py`](rbac_service/settings.py)

## 2. User Model Implementation

- [ ] 2.1 Create custom UserManager in `users/managers.py` with create_user() and create_superuser() methods
- [ ] 2.2 Create custom User model in `users/models.py` extending AbstractBaseUser
- [ ] 2.3 Add email field as CharField with unique=True, max_length=255
- [ ] 2.4 Add first_name field as CharField with max_length=255
- [ ] 2.5 Add middle_name field as CharField with max_length=255 (optional)
- [ ] 2.6 Add last_name field as CharField with max_length=255
- [ ] 2.7 Add is_active, is_staff, is_superuser boolean fields with appropriate defaults
- [ ] 2.8 Add date_joined DateTimeField with auto_now_add=True
- [ ] 2.9 Set USERNAME_FIELD = 'email' on the User model
- [ ] 2.10 Configure REQUIRED_FIELDS as empty list

## 3. Django Admin Integration

- [ ] 3.1 Create custom UserAdmin class in `users/admin.py`
- [ ] 3.2 Register the User model with the custom UserAdmin
- [ ] 3.3 Configure admin display for email, first_name, middle_name, last_name
- [ ] 3.4 Configure admin filters for is_active and is_staff

## 4. Database Migration

- [ ] 4.1 Create initial migrations for the users app: `uv run manage.py makemigrations users`
- [ ] 4.2 Run migrations: `uv run manage.py migrate`
- [ ] 4.3 Verify the users_user table is created in the database

## 5. Testing

- [ ] 5.1 Write unit tests for UserManager.create_user()
- [ ] 5.2 Write unit tests for UserManager.create_superuser()
- [ ] 5.3 Write unit tests for User model field validation
- [ ] 5.4 Write unit tests for email uniqueness constraint
- [ ] 5.5 Write integration tests for Django admin user creation
- [ ] 5.6 Run all tests with pytest: `pytest`
- [ ] 5.7 Verify code coverage meets 80% threshold

## 6. Documentation

- [ ] 6.1 Add docstrings to UserManager methods
- [ ] 6.2 Add docstrings to User model
- [ ] 6.3 Update README.md with custom user model information
- [ ] 6.4 Document the AUTH_USER_MODEL setting requirement

## 7. Validation

- [ ] 7.1 Verify Django admin can create users
- [ ] 7.2 Verify Django admin can modify users
- [ ] 7.3 Verify Django admin can delete users
- [ ] 7.4 Verify authentication works with email and password
- [ ] 7.5 Run `ruff check` for linting
- [ ] 7.6 Run `ruff format` for code formatting
