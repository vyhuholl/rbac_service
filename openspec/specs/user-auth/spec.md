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

### Requirement: User Registration
The system SHALL provide an API endpoint for user registration that accepts email, password, first_name, middle_name (optional), and last_name fields. The password SHALL be hashed before storage and the email SHALL be validated for uniqueness.

#### Scenario: Successful user registration
- **WHEN** a POST request is sent to the registration endpoint with valid email, password, first_name, and last_name
- **THEN** a new user is created
- **AND** the password is hashed
- **AND** the email is stored as the unique identifier
- **AND** is_active is set to True
- **AND** a 201 Created status is returned

#### Scenario: User registration with duplicate email
- **WHEN** a POST request is sent to the registration endpoint with an email that already exists
- **THEN** the registration fails
- **AND** a 400 Bad Request status is returned
- **AND** an error message indicates the email is already registered

#### Scenario: User registration without required fields
- **WHEN** a POST request is sent to the registration endpoint without required fields (email, password, first_name, last_name)
- **THEN** the registration fails
- **AND** a 400 Bad Request status is returned
- **AND** validation errors indicate missing fields

### Requirement: User Login
The system SHALL provide an API endpoint for user authentication that accepts email and password credentials. Upon successful authentication, the system SHALL return an authentication token or session identifier.

#### Scenario: Successful user login
- **WHEN** a POST request is sent to the login endpoint with valid email and password
- **THEN** authentication succeeds
- **AND** an authentication token or session is returned
- **AND** a 200 OK status is returned

#### Scenario: User login with invalid credentials
- **WHEN** a POST request is sent to the login endpoint with invalid email or password
- **THEN** authentication fails
- **AND** no token or session is returned
- **AND** a 401 Unauthorized status is returned

#### Scenario: User login with inactive account
- **WHEN** a POST request is sent to the login endpoint with credentials for an inactive user (is_active=False)
- **THEN** authentication fails
- **AND** a 401 Unauthorized status is returned
- **AND** an error message indicates the account is inactive

### Requirement: User Logout
The system SHALL provide an API endpoint for user logout that invalidates the current authentication session or token. The endpoint SHALL require authentication.

#### Scenario: Successful user logout
- **WHEN** a POST request is sent to the logout endpoint with valid authentication
- **THEN** the authentication session or token is invalidated
- **AND** a 200 OK status is returned

#### Scenario: Logout without authentication
- **WHEN** a POST request is sent to the logout endpoint without authentication
- **THEN** the logout fails
- **AND** a 401 Unauthorized status is returned

### Requirement: Account Deletion
The system SHALL provide an API endpoint for soft-deleting user accounts. When a user requests account deletion, the is_active field SHALL be set to False. The endpoint SHALL require authentication.

#### Scenario: Successful account deletion
- **WHEN** a DELETE request is sent to the account deletion endpoint with valid authentication
- **THEN** the user's is_active field is set to False
- **AND** the user record remains in the database
- **AND** a 200 OK or 204 No Content status is returned

#### Scenario: Account deletion without authentication
- **WHEN** a DELETE request is sent to the account deletion endpoint without authentication
- **THEN** the deletion fails
- **AND** a 401 Unauthorized status is returned

#### Scenario: Login attempt after account deletion
- **WHEN** a user with is_active=False attempts to login
- **THEN** authentication fails
- **AND** a 401 Unauthorized status is returned

### Requirement: User Profile Update
The system SHALL provide an API endpoint for authenticated users to update their profile information. Users SHALL be able to modify first_name, middle_name, and last_name fields. The email field SHALL NOT be modifiable through this endpoint.

#### Scenario: Successful profile update
- **WHEN** a PATCH or PUT request is sent to the profile update endpoint with valid authentication and profile data
- **THEN** the user's profile is updated with the provided fields
- **AND** a 200 OK status is returned
- **AND** the updated user data is returned in the response

#### Scenario: Profile update without authentication
- **WHEN** a PATCH or PUT request is sent to the profile update endpoint without authentication
- **THEN** the update fails
- **AND** a 401 Unauthorized status is returned

#### Scenario: Profile update with email field
- **WHEN** a request to the profile update endpoint includes an email field
- **THEN** the email field is ignored or rejected
- **AND** the email is not modified
- **AND** other valid fields are updated

### Requirement: API Authentication
The system SHALL use Django REST Framework's authentication mechanisms for protecting API endpoints. Protected endpoints SHALL require valid authentication.

#### Scenario: Accessing protected endpoint with valid authentication
- **WHEN** a request is made to a protected endpoint with valid authentication
- **THEN** the request is processed
- **AND** the appropriate response is returned

#### Scenario: Accessing protected endpoint without authentication
- **WHEN** a request is made to a protected endpoint without authentication
- **THEN** the request is rejected
- **AND** a 401 Unauthorized status is returned

