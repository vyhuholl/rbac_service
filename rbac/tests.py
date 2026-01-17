from django.test import TestCase
from django.db import IntegrityError
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import Client

from .models import AccessRoleRule, BusinessElement, Role
from .admin import AccessRoleRuleAdmin, BusinessElementAdmin, RoleAdmin

User = get_user_model()


class RoleModelTest(TestCase):
    """Test cases for Role model."""

    def test_role_creation_with_name_and_description(self):
        """Test creating role with name and description."""
        role = Role.objects.create(
            name='Admin', description='Administrator role'
        )
        self.assertEqual(role.name, 'Admin')
        self.assertEqual(role.description, 'Administrator role')
        self.assertIsNotNone(role.id)
        self.assertIsNotNone(role.created_at)
        self.assertIsNotNone(role.updated_at)

    def test_role_creation_with_name_only(self):
        """Test creating role with only name."""
        role = Role.objects.create(name='User')
        self.assertEqual(role.name, 'User')
        self.assertIsNone(role.description)

    def test_role_name_uniqueness(self):
        """Test role name uniqueness constraint."""
        Role.objects.create(name='Manager')
        with self.assertRaises(IntegrityError):
            Role.objects.create(name='Manager')

    def test_role_str_method(self):
        """Test Role __str__ method."""
        role = Role.objects.create(name='Editor')
        self.assertEqual(str(role), 'Editor')


class BusinessElementModelTest(TestCase):
    """Test cases for BusinessElement model."""

    def test_business_element_creation_with_all_fields(self):
        """Test creating business element with all fields."""
        element = BusinessElement.objects.create(
            name='UserProfile', description='User profile data'
        )
        self.assertEqual(element.name, 'UserProfile')
        self.assertEqual(element.description, 'User profile data')
        self.assertIsNotNone(element.id)
        self.assertIsNotNone(element.created_at)
        self.assertIsNotNone(element.updated_at)

    def test_business_element_name_uniqueness(self):
        """Test business element name uniqueness constraint."""
        BusinessElement.objects.create(name='Invoice')
        with self.assertRaises(IntegrityError):
            BusinessElement.objects.create(name='Invoice')

    def test_business_element_str_method(self):
        """Test BusinessElement __str__ method."""
        element = BusinessElement.objects.create(name='Product')
        self.assertEqual(str(element), 'Product')


class AccessRoleRuleModelTest(TestCase):
    """Test cases for AccessRoleRule model."""

    def setUp(self):
        """Set up test data."""
        self.role = Role.objects.create(name='Viewer')
        self.element = BusinessElement.objects.create(name='Report')

    def test_access_rule_creation_with_all_permissions(self):
        """Test creating access rule with all permission fields."""
        rule = AccessRoleRule.objects.create(
            role=self.role,
            element=self.element,
            read_permission=True,
            read_all_permission=False,
            create_permission=True,
            update_permission=False,
            update_all_permission=False,
            delete_permission=True,
            delete_all_permission=False,
        )
        self.assertEqual(rule.role, self.role)
        self.assertEqual(rule.element, self.element)
        self.assertTrue(rule.read_permission)
        self.assertFalse(rule.read_all_permission)
        self.assertTrue(rule.create_permission)
        self.assertFalse(rule.update_permission)
        self.assertFalse(rule.update_all_permission)
        self.assertTrue(rule.delete_permission)
        self.assertFalse(rule.delete_all_permission)
        self.assertIsNotNone(rule.id)

    def test_access_rule_creation_with_partial_permissions(self):
        """Test creating access rule with only some permission fields."""
        rule = AccessRoleRule.objects.create(
            role=self.role, element=self.element, read_permission=True
        )
        self.assertTrue(rule.read_permission)
        self.assertFalse(rule.read_all_permission)
        self.assertFalse(rule.create_permission)
        self.assertFalse(rule.update_permission)
        self.assertFalse(rule.update_all_permission)
        self.assertFalse(rule.delete_permission)
        self.assertFalse(rule.delete_all_permission)

    def test_unique_constraint_on_role_and_element(self):
        """Test unique constraint on (role, element) combination."""
        AccessRoleRule.objects.create(role=self.role, element=self.element)
        with self.assertRaises(IntegrityError):
            AccessRoleRule.objects.create(role=self.role, element=self.element)

    def test_access_rule_str_method(self):
        """Test AccessRoleRule __str__ method."""
        rule = AccessRoleRule.objects.create(
            role=self.role, element=self.element
        )
        self.assertEqual(str(rule), 'Viewer - Report')

    def test_different_roles_can_have_rules_for_same_element(self):
        """Test that different roles can have rules for the same element."""
        role2 = Role.objects.create(name='Editor')
        rule1 = AccessRoleRule.objects.create(
            role=self.role, element=self.element, read_permission=True
        )
        rule2 = AccessRoleRule.objects.create(
            role=role2, element=self.element, create_permission=True
        )
        self.assertNotEqual(rule1.role, rule2.role)
        self.assertEqual(rule1.element, rule2.element)

    def test_same_role_can_have_rules_for_different_elements(self):
        """Test that the same role can have rules for different elements."""
        element2 = BusinessElement.objects.create(name='Dashboard')
        rule1 = AccessRoleRule.objects.create(
            role=self.role, element=self.element, read_permission=True
        )
        rule2 = AccessRoleRule.objects.create(
            role=self.role, element=element2, create_permission=True
        )
        self.assertEqual(rule1.role, rule2.role)
        self.assertNotEqual(rule1.element, rule2.element)


class RoleAdminTest(TestCase):
    """Integration tests for Role admin."""

    def setUp(self):
        """Set up test data."""
        self.site = AdminSite()
        self.role_admin = RoleAdmin(Role, self.site)
        self.superuser = User.objects.create_superuser(
            email='admin@test.com',
            password='password',
            first_name='Admin',
            last_name='User',
        )
        self.client = Client()
        self.client.force_login(self.superuser)

    def test_role_admin_list_display(self):
        """Test RoleAdmin list_display configuration."""
        self.assertIn('name', self.role_admin.list_display)
        self.assertIn('description', self.role_admin.list_display)

    def test_role_admin_search_fields(self):
        """Test RoleAdmin search_fields configuration."""
        self.assertIn('name', self.role_admin.search_fields)


class BusinessElementAdminTest(TestCase):
    """Integration tests for BusinessElement admin."""

    def setUp(self):
        """Set up test data."""
        self.site = AdminSite()
        self.element_admin = BusinessElementAdmin(BusinessElement, self.site)
        self.superuser = User.objects.create_superuser(
            email='admin@test.com',
            password='password',
            first_name='Admin',
            last_name='User',
        )
        self.client = Client()
        self.client.force_login(self.superuser)

    def test_business_element_admin_list_display(self):
        """Test BusinessElementAdmin list_display configuration."""
        self.assertIn('name', self.element_admin.list_display)
        self.assertIn('description', self.element_admin.list_display)

    def test_business_element_admin_search_fields(self):
        """Test BusinessElementAdmin search_fields configuration."""
        self.assertIn('name', self.element_admin.search_fields)


class AccessRoleRuleAdminTest(TestCase):
    """Integration tests for AccessRoleRule admin."""

    def setUp(self):
        """Set up test data."""
        self.site = AdminSite()
        self.rule_admin = AccessRoleRuleAdmin(AccessRoleRule, self.site)
        self.superuser = User.objects.create_superuser(
            email='admin@test.com',
            password='password',
            first_name='Admin',
            last_name='User',
        )
        self.client = Client()
        self.client.force_login(self.superuser)
        self.role = Role.objects.create(name='TestRole')
        self.element = BusinessElement.objects.create(name='TestElement')

    def test_access_role_rule_admin_list_display(self):
        """Test AccessRoleRuleAdmin list_display configuration."""
        self.assertIn('role', self.rule_admin.list_display)
        self.assertIn('element', self.rule_admin.list_display)
        self.assertIn('read_permission', self.rule_admin.list_display)
        self.assertIn('read_all_permission', self.rule_admin.list_display)
        self.assertIn('create_permission', self.rule_admin.list_display)
        self.assertIn('update_permission', self.rule_admin.list_display)
        self.assertIn('update_all_permission', self.rule_admin.list_display)
        self.assertIn('delete_permission', self.rule_admin.list_display)
        self.assertIn('delete_all_permission', self.rule_admin.list_display)

    def test_access_role_rule_admin_list_filter(self):
        """Test AccessRoleRuleAdmin list_filter configuration."""
        self.assertIn('role', self.rule_admin.list_filter)
        self.assertIn('element', self.rule_admin.list_filter)
