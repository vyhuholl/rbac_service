## 1. Serializers

- [x] 1.1 Create `users/serializers.py` file
- [x] 1.2 Create UserRegistrationSerializer with email, password, first_name, middle_name, last_name fields
- [x] 1.3 Create UserLoginSerializer with email and password fields
- [x] 1.4 Create UserUpdateSerializer with optional fields for first_name, middle_name, last_name
- [x] 1.5 Add password validation to UserRegistrationSerializer
- [x] 1.6 Add email uniqueness validation to UserRegistrationSerializer

## 2. Views

- [x] 2.1 Create RegisterView using APIView or GenericAPIView
- [x] 2.2 Create LoginView using ObtainAuthToken or custom implementation
- [x] 2.3 Create LogoutView to invalidate user session/token
- [x] 2.4 Create AccountDeleteView to soft-delete user (set is_active=False)
- [x] 2.5 Create UserUpdateView to allow users to update their profile information
- [x] 2.6 Add IsAuthenticated permission to protected views (logout, delete, update)
- [x] 2.7 Add appropriate error handling and validation

## 3. URL Configuration

- [x] 3.1 Create `users/urls.py` file
- [x] 3.2 Configure URL path for register endpoint
- [x] 3.3 Configure URL path for login endpoint
- [x] 3.4 Configure URL path for logout endpoint
- [x] 3.5 Configure URL path for account deletion endpoint
- [x] 3.6 Configure URL path for user update endpoint
- [x] 3.7 Include users URLs in main [`rbac_service/urls.py`](rbac_service/urls.py)

## 4. Testing

- [x] 4.1 Write unit tests for UserRegistrationSerializer
- [x] 4.2 Write unit tests for UserLoginSerializer
- [x] 4.3 Write unit tests for UserUpdateSerializer
- [x] 4.4 Write integration tests for RegisterView
- [x] 4.5 Write integration tests for LoginView
- [x] 4.6 Write integration tests for LogoutView
- [x] 4.7 Write integration tests for AccountDeleteView
- [x] 4.8 Write integration tests for UserUpdateView
- [x] 4.9 Run all tests with pytest
- [x] 4.10 Verify code coverage meets 80% threshold

## 5. Validation

- [x] 5.1 Verify register endpoint creates new user with valid data
- [x] 5.2 Verify register endpoint rejects duplicate email
- [x] 5.3 Verify login endpoint returns authentication token
- [x] 5.4 Verify login endpoint rejects invalid credentials
- [x] 5.5 Verify logout endpoint invalidates session
- [x] 5.6 Verify account deletion sets is_active to False
- [x] 5.7 Verify user update modifies only allowed fields
- [x] 5.8 Run `ruff check` for linting
- [x] 5.9 Run `ruff format` for code formatting
