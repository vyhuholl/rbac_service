# user-auth Specification

## Purpose
TBD - created by archiving change add-custom-user-model. Update Purpose after archive.
## Requirements
### Requirement: Custom User Model
The system SHALL provide a custom User model that extends Django's AbstractBaseUser with the following fields: first name, middle name, last name, and email address. The email field SHALL serve as the unique username field for authentication.

#### Scenario: User creation with all fields
- **WHEN** a new user is created with first_name, middle_name, last_name, and email
- **THEN** the user is stored successfully with all fields populated
- **AND** the email is stored as the unique identifier
- **AND** a password hash is generated for authentication

#### Scenario: User creation without middle name
- **WHEN** a new user is created with first_name, last_name, and email but no middle_name
- **THEN** the user is stored successfully
- **AND** the middle_name field is null or empty

#### Scenario: Email uniqueness validation
- **WHEN** a user is created with an email that already exists in the system
- **THEN** the creation fails with a uniqueness validation error
- **AND** no duplicate user record is created

#### Scenario: Email as username for authentication
- **WHEN** a user attempts to authenticate using their email and password
- **THEN** the system authenticates the user using the email field as the username
- **AND** authentication succeeds with valid credentials
- **AND** authentication fails with invalid credentials

### Requirement: User Model Fields
The custom User model SHALL include the following fields with specified characteristics:

- `email`: CharField, unique=True, max_length=255, serves as USERNAME_FIELD
- `first_name`: CharField, max_length=255, optional
- `middle_name`: CharField, max_length=255, optional
- `last_name`: CharField, max_length=255, optional
- `is_active`: BooleanField, default=True
- `is_staff`: BooleanField, default=False
- `is_superuser`: BooleanField, default=False
- `date_joined`: DateTimeField, auto_now_add=True

#### Scenario: User model field types
- **WHEN** the User model is inspected
- **THEN** all required fields are present with correct types
- **AND** the email field is configured as the USERNAME_FIELD

#### Scenario: Default values for boolean fields
- **WHEN** a new user is created
- **THEN** is_active defaults to True
- **AND** is_staff defaults to False
- **AND** is_superuser defaults to False

#### Scenario: Date joined auto-population
- **WHEN** a new user is created
- **THEN** the date_joined field is automatically set to the current datetime

### Requirement: User Manager
The system SHALL provide a custom UserManager that implements create_user() and create_superuser() methods for user creation with proper password hashing.

#### Scenario: Create regular user via manager
- **WHEN** UserManager.create_user() is called with email and password
- **THEN** a user is created with the provided email
- **AND** the password is properly hashed
- **AND** is_staff and is_superuser are set to False
- **AND** is_active is set to True

#### Scenario: Create superuser via manager
- **WHEN** UserManager.create_superuser() is called with email and password
- **THEN** a user is created with the provided email
- **AND** the password is properly hashed
- **AND** is_staff is set to True
- **AND** is_superuser is set to True
- **AND** is_active is set to True

#### Scenario: User creation without password raises error
- **WHEN** UserManager.create_user() is called without a password
- **THEN** a ValueError is raised indicating password is required

### Requirement: Django Settings Configuration
The system SHALL configure AUTH_USER_MODEL to point to the custom User model before any migrations are created.

#### Scenario: AUTH_USER_MODEL setting
- **WHEN** Django settings are loaded
- **THEN** AUTH_USER_MODEL is set to 'users.User'
- **AND** the custom User model is used throughout the application

#### Scenario: Users app in INSTALLED_APPS
- **WHEN** Django settings are loaded
- **THEN** the 'users' app is included in INSTALLED_APPS
- **AND** the app is properly registered with Django

### Requirement: Django Admin Integration
The custom User model SHALL be registered with Django's admin interface for management through the admin panel.

#### Scenario: User model in admin
- **WHEN** the Django admin is accessed
- **THEN** the User model is visible in the admin interface
- **AND** users can be created, viewed, and modified through the admin
- **AND** user passwords can be set through the admin interface

