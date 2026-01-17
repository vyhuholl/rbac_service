from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserUpdateSerializer,
)


class UserManagerTestCase(TestCase):
    """Test cases for UserManager methods."""

    def test_create_user_with_email_and_password(self):
        """Test creating a user with email and password."""
        user = User.objects.create_user(
            email='test@example.com', password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email_raises_error(self):
        """Test that creating a user without email raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='testpass123')

    def test_create_user_without_password_raises_error(self):
        """Test that creating a user without password raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_user(email='test@example.com', password=None)

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email='admin@example.com', password='adminpass123'
        )
        self.assertEqual(user.email, 'admin@example.com')
        self.assertTrue(user.check_password('adminpass123'))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_superuser_without_is_staff_raises_error(self):
        """Test that creating superuser with is_staff=False raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='adminpass123',
                is_staff=False,
            )

    def test_create_superuser_without_is_superuser_raises_error(self):
        """Test that creating superuser with is_superuser=False raises ValueError."""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='adminpass123',
                is_superuser=False,
            )

    def test_email_normalization(self):
        """Test that email is normalized when creating user."""
        user = User.objects.create_user(
            email='Test.User@EXAMPLE.COM', password='testpass123'
        )
        self.assertEqual(user.email, 'Test.User@example.com')


class UserModelTestCase(TestCase):
    """Test cases for User model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email='john.doe@example.com',
            password='testpass123',
            first_name='John',
            middle_name='Michael',
            last_name='Doe',
        )

    def test_user_creation_with_all_fields(self):
        """Test that user is created with all fields."""
        self.assertEqual(self.user.email, 'john.doe@example.com')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.middle_name, 'Michael')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertIsNotNone(self.user.date_joined)

    def test_user_creation_without_middle_name(self):
        """Test that user can be created without middle name."""
        user = User.objects.create_user(
            email='jane.doe@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Doe',
        )
        self.assertEqual(user.middle_name, '')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')

    def test_email_uniqueness(self):
        """Test that email must be unique."""
        with self.assertRaises(Exception):  # IntegrityError from database
            User.objects.create_user(
                email='john.doe@example.com',  # Same email as self.user
                password='differentpass',
            )

    def test_string_representation(self):
        """Test the string representation of User."""
        expected = 'John Doe (john.doe@example.com)'
        self.assertEqual(str(self.user), expected)

    def test_username_field_is_email(self):
        """Test that USERNAME_FIELD is set to email."""
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_required_fields(self):
        """Test that REQUIRED_FIELDS is empty."""
        self.assertEqual(User.REQUIRED_FIELDS, [])

    def test_has_perm_superuser(self):
        """Test has_perm method for superuser."""
        superuser = User.objects.create_superuser(
            email='super@example.com', password='superpass'
        )
        self.assertTrue(superuser.has_perm('any_permission'))

    def test_has_perms_superuser(self):
        """Test has_perms method for superuser."""
        superuser = User.objects.create_superuser(
            email='super@example.com', password='superpass'
        )
        self.assertTrue(superuser.has_perms(['perm1', 'perm2']))

    def test_has_module_perms_superuser(self):
        """Test has_module_perms method for superuser."""
        superuser = User.objects.create_superuser(
            email='super@example.com', password='superpass'
        )
        self.assertTrue(superuser.has_module_perms('any_app'))

    def test_has_perm_regular_user(self):
        """Test has_perm method for regular user."""
        self.assertFalse(self.user.has_perm('any_permission'))

    def test_has_perms_regular_user(self):
        """Test has_perms method for regular user."""
        self.assertFalse(self.user.has_perms(['perm1', 'perm2']))

    def test_has_module_perms_regular_user(self):
        """Test has_module_perms method for regular user."""
        self.assertFalse(self.user.has_module_perms('any_app'))


class UserRegistrationSerializerTestCase(TestCase):
    """Test cases for UserRegistrationSerializer."""

    def test_valid_registration_data(self):
        """Test serializer with valid registration data."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_duplicate_email_registration(self):
        """Test that duplicate email raises validation error."""
        User.objects.create_user(
            email='existing@example.com', password='pass123'
        )
        data = {
            'email': 'existing@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_password_mismatch(self):
        """Test that mismatched passwords raise validation error."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'differentpass',
            'first_name': 'Test',
            'last_name': 'User',
        }
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password_confirm', serializer.errors)


class UserLoginSerializerTestCase(TestCase):
    """Test cases for UserLoginSerializer."""

    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            email='test@example.com', password='testpass123'
        )

    def test_valid_login_credentials(self):
        """Test serializer with valid login credentials."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        serializer = UserLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['user'], self.user)

    def test_invalid_email(self):
        """Test serializer with invalid email."""
        data = {
            'email': 'wrong@example.com',
            'password': 'testpass123',
        }
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_invalid_password(self):
        """Test serializer with invalid password."""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpass',
        }
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_inactive_user_login(self):
        """Test that inactive user cannot login."""
        self.user.is_active = False
        self.user.save()
        data = {
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        serializer = UserLoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class UserUpdateSerializerTestCase(TestCase):
    """Test cases for UserUpdateSerializer."""

    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
        )

    def test_update_first_name(self):
        """Test updating first name."""
        data = {'first_name': 'Jane'}
        serializer = UserUpdateSerializer(self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Jane')

    def test_update_multiple_fields(self):
        """Test updating multiple fields."""
        data = {
            'first_name': 'Jane',
            'middle_name': 'Marie',
            'last_name': 'Smith',
        }
        serializer = UserUpdateSerializer(self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.middle_name, 'Marie')
        self.assertEqual(self.user.last_name, 'Smith')


class UserAPITestCase(APITestCase):
    """Test cases for user API views."""

    def setUp(self):
        """Set up test user."""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
        )
        self.token = Token.objects.create(user=self.user)

    def test_register_view_success(self):
        """Test successful user registration."""
        data = {
            'email': 'new@example.com',
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
        }
        response = self.client.post(
            '/api/users/register/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['email'], 'new@example.com')

    def test_register_view_duplicate_email(self):
        """Test registration with duplicate email."""
        data = {
            'email': 'test@example.com',  # Already exists
            'password': 'newpass123',
            'password_confirm': 'newpass123',
            'first_name': 'New',
            'last_name': 'User',
        }
        response = self.client.post(
            '/api/users/register/', data, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view_success(self):
        """Test successful user login."""
        data = {
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        response = self.client.post('/api/users/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_view_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'email': 'test@example.com',
            'password': 'wrongpass',
        }
        response = self.client.post('/api/users/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_view_authenticated(self):
        """Test logout with authenticated user."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post('/api/users/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Token should be deleted
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())

    def test_logout_view_unauthenticated(self):
        """Test logout without authentication."""
        response = self.client.post('/api/users/logout/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_account_delete_authenticated(self):
        """Test account deletion with authenticated user."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete('/api/users/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # User should be inactive
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        # Token should be deleted
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_account_delete_unauthenticated(self):
        """Test account deletion without authentication."""
        response = self.client.delete('/api/users/delete/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_update_authenticated(self):
        """Test user profile update with authenticated user."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        data = {'first_name': 'Jane', 'last_name': 'Smith'}
        response = self.client.patch('/api/users/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['first_name'], 'Jane')
        self.assertEqual(response.data['user']['last_name'], 'Smith')

    def test_user_update_unauthenticated(self):
        """Test user profile update without authentication."""
        data = {'first_name': 'Jane'}
        response = self.client.patch('/api/users/update/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
