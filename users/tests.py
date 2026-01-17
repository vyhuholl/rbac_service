from django.test import TestCase

from .models import User


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
