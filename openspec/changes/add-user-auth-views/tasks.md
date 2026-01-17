## 1. Serializers

- [ ] 1.1 Create `users/serializers.py` file
- [ ] 1.2 Create UserRegistrationSerializer with email, password, first_name, middle_name, last_name fields
- [ ] 1.3 Create UserLoginSerializer with email and password fields
- [ ] 1.4 Create UserUpdateSerializer with optional fields for first_name, middle_name, last_name
- [ ] 1.5 Add password validation to UserRegistrationSerializer
- [ ] 1.6 Add email uniqueness validation to UserRegistrationSerializer

## 2. Views

- [ ] 2.1 Create RegisterView using APIView or GenericAPIView
- [ ] 2.2 Create LoginView using ObtainAuthToken or custom implementation
- [ ] 2.3 Create LogoutView to invalidate user session/token
- [ ] 2.4 Create AccountDeleteView to soft-delete user (set is_active=False)
- [ ] 2.5 Create UserUpdateView to allow users to update their profile information
- [ ] 2.6 Add IsAuthenticated permission to protected views (logout, delete, update)
- [ ] 2.7 Add appropriate error handling and validation

## 3. URL Configuration

- [ ] 3.1 Create `users/urls.py` file
- [ ] 3.2 Configure URL path for register endpoint
- [ ] 3.3 Configure URL path for login endpoint
- [ ] 3.4 Configure URL path for logout endpoint
- [ ] 3.5 Configure URL path for account deletion endpoint
- [ ] 3.6 Configure URL path for user update endpoint
- [ ] 3.7 Include users URLs in main [`rbac_service/urls.py`](rbac_service/urls.py)

## 4. Testing

- [ ] 4.1 Write unit tests for UserRegistrationSerializer
- [ ] 4.2 Write unit tests for UserLoginSerializer
- [ ] 4.3 Write unit tests for UserUpdateSerializer
- [ ] 4.4 Write integration tests for RegisterView
- [ ] 4.5 Write integration tests for LoginView
- [ ] 4.6 Write integration tests for LogoutView
- [ ] 4.7 Write integration tests for AccountDeleteView
- [ ] 4.8 Write integration tests for UserUpdateView
- [ ] 4.9 Run all tests with pytest
- [ ] 4.10 Verify code coverage meets 80% threshold

## 5. Validation

- [ ] 5.1 Verify register endpoint creates new user with valid data
- [ ] 5.2 Verify register endpoint rejects duplicate email
- [ ] 5.3 Verify login endpoint returns authentication token
- [ ] 5.4 Verify login endpoint rejects invalid credentials
- [ ] 5.5 Verify logout endpoint invalidates session
- [ ] 5.6 Verify account deletion sets is_active to False
- [ ] 5.7 Verify user update modifies only allowed fields
- [ ] 5.8 Run `ruff check` for linting
- [ ] 5.9 Run `ruff format` for code formatting
