## ADDED Requirements

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
