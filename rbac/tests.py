from django.test import TestCase
from django.db import IntegrityError
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APITestCase
from rest_framework import status

from .models import AccessRoleRule, BusinessElement, Role, UserRole
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


class UserRoleModelTest(TestCase):
    """Test cases for UserRole model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email='test@example.com',
            password='password',
            first_name='Test',
            last_name='User',
        )
        self.role = Role.objects.create(name='TestRole')

    def test_user_role_creation(self):
        """Test creating user-role association."""
        user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.assertEqual(user_role.user, self.user)
        self.assertEqual(user_role.role, self.role)
        self.assertIsNotNone(user_role.id)
        self.assertIsNotNone(user_role.created_at)

    def test_unique_constraint_on_user_and_role(self):
        """Test unique constraint on (user, role) combination."""
        UserRole.objects.create(user=self.user, role=self.role)
        with self.assertRaises(IntegrityError):
            UserRole.objects.create(user=self.user, role=self.role)

    def test_user_role_str_method(self):
        """Test UserRole __str__ method."""
        user_role = UserRole.objects.create(user=self.user, role=self.role)
        self.assertEqual(
            str(user_role), 'Test User (test@example.com) - TestRole'
        )


class AccessViewTest(APITestCase):
    """Test cases for AccessView."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email='user@test.com',
            password='password',
            first_name='Test',
            last_name='User',
        )
        self.role = Role.objects.create(name='Reader')
        self.element = BusinessElement.objects.create(
            name='Document', description='A test document'
        )
        self.user_role = UserRole.objects.create(
            user=self.user, role=self.role
        )
        self.access_rule = AccessRoleRule.objects.create(
            role=self.role,
            element=self.element,
            read_permission=True,
            create_permission=False,
        )

    def test_successful_access(self):
        """Test successful access when user has required permissions."""
        url = '/api/rbac/access/'
        params = {
            'user_id': str(self.user.id),
            'resource': 'Document',
            'permissions': 'read',
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Document')
        self.assertEqual(response.data['description'], 'A test document')

    def test_user_not_found(self):
        """Test 401 when user does not exist."""
        url = '/api/rbac/access/'
        params = {
            'user_id': -1,
            'resource': 'Document',
            'permissions': 'read',
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_insufficient_permissions(self):
        """Test 403 when user lacks required permissions."""
        url = '/api/rbac/access/'
        params = {
            'user_id': str(self.user.id),
            'resource': 'Document',
            'permissions': 'create',  # User has read but not create
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)

    def test_resource_not_found(self):
        """Test 403 when resource does not exist."""
        url = '/api/rbac/access/'
        params = {
            'user_id': str(self.user.id),
            'resource': 'NonExistent',
            'permissions': 'read',
        }
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('error', response.data)

    def test_missing_parameters(self):
        """Test 400 when required parameters are missing."""
        url = '/api/rbac/access/'
        params = {
            'user_id': str(self.user.id)
        }  # Missing resource and permissions
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class IsSuperuserPermissionTest(APITestCase):
    """Test cases for IsSuperuser permission class."""

    def setUp(self):
        """Set up test data."""
        self.superuser = User.objects.create_superuser(
            email='super@test.com',
            password='password',
            first_name='Super',
            last_name='User',
        )
        self.regular_user = User.objects.create_user(
            email='regular@test.com',
            password='password',
            first_name='Regular',
            last_name='User',
        )

    def test_superuser_has_permission(self):
        """Test that superuser has permission."""
        self.client.force_authenticate(user=self.superuser)
        url = '/api/rbac/roles/'
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_regular_user_denied_permission(self):
        """Test that regular user is denied permission."""
        self.client.force_authenticate(user=self.regular_user)
        url = '/api/rbac/roles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_denied_permission(self):
        """Test that unauthenticated user is denied permission."""
        url = '/api/rbac/roles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RoleViewSetTest(APITestCase):
    """Test cases for RoleViewSet."""

    def setUp(self):
        """Set up test data."""
        self.superuser = User.objects.create_superuser(
            email='super@test.com',
            password='password',
            first_name='Super',
            last_name='User',
        )
        self.regular_user = User.objects.create_user(
            email='regular@test.com',
            password='password',
            first_name='Regular',
            last_name='User',
        )
        self.client.force_authenticate(user=self.superuser)

    def test_list_roles(self):
        """Test listing all roles."""
        Role.objects.create(name='TestRole', description='Test description')
        url = '/api/rbac/roles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'TestRole')
        self.assertEqual(response.data[0]['description'], 'Test description')

    def test_create_role(self):
        """Test creating a new role."""
        url = '/api/rbac/roles/'
        data = {'name': 'NewRole', 'description': 'New role description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'NewRole')
        self.assertEqual(response.data['description'], 'New role description')
        self.assertTrue(Role.objects.filter(name='NewRole').exists())

    def test_retrieve_role(self):
        """Test retrieving a specific role."""
        role = Role.objects.create(
            name='RetrieveRole', description='Retrieve me'
        )
        url = f'/api/rbac/roles/{role.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'RetrieveRole')
        self.assertEqual(response.data['description'], 'Retrieve me')

    def test_update_role(self):
        """Test updating a role."""
        role = Role.objects.create(
            name='UpdateRole', description='Old description'
        )
        url = f'/api/rbac/roles/{role.id}/'
        data = {'name': 'UpdatedRole', 'description': 'Updated description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'UpdatedRole')
        self.assertEqual(response.data['description'], 'Updated description')
        role.refresh_from_db()
        self.assertEqual(role.name, 'UpdatedRole')
        self.assertEqual(role.description, 'Updated description')

    def test_delete_role(self):
        """Test deleting a role."""
        role = Role.objects.create(
            name='DeleteRole', description='To be deleted'
        )
        url = f'/api/rbac/roles/{role.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Role.objects.filter(name='DeleteRole').exists())

    def test_non_superuser_denied_access(self):
        """Test that non-superuser is denied access."""
        self.client.force_authenticate(user=self.regular_user)
        url = '/api/rbac/roles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_denied_access(self):
        """Test that unauthenticated user is denied access."""
        self.client.force_authenticate(user=None)
        url = '/api/rbac/roles/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class BusinessElementViewSetTest(APITestCase):
    """Test cases for BusinessElementViewSet."""

    def setUp(self):
        """Set up test data."""
        self.superuser = User.objects.create_superuser(
            email='super@test.com',
            password='password',
            first_name='Super',
            last_name='User',
        )
        self.client.force_authenticate(user=self.superuser)

    def test_list_business_elements(self):
        """Test listing all business elements."""
        BusinessElement.objects.create(
            name='TestElement', description='Test description'
        )
        url = '/api/rbac/business-elements/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'TestElement')

    def test_create_business_element(self):
        """Test creating a new business element."""
        url = '/api/rbac/business-elements/'
        data = {'name': 'NewElement', 'description': 'New element description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'NewElement')
        self.assertTrue(
            BusinessElement.objects.filter(name='NewElement').exists()
        )

    def test_retrieve_business_element(self):
        """Test retrieving a specific business element."""
        element = BusinessElement.objects.create(
            name='RetrieveElement', description='Retrieve me'
        )
        url = f'/api/rbac/business-elements/{element.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'RetrieveElement')

    def test_update_business_element(self):
        """Test updating a business element."""
        element = BusinessElement.objects.create(
            name='UpdateElement', description='Old description'
        )
        url = f'/api/rbac/business-elements/{element.id}/'
        data = {'name': 'UpdatedElement', 'description': 'Updated description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'UpdatedElement')
        element.refresh_from_db()
        self.assertEqual(element.name, 'UpdatedElement')

    def test_delete_business_element(self):
        """Test deleting a business element."""
        element = BusinessElement.objects.create(
            name='DeleteElement', description='To be deleted'
        )
        url = f'/api/rbac/business-elements/{element.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            BusinessElement.objects.filter(name='DeleteElement').exists()
        )


class AccessRoleRuleViewSetTest(APITestCase):
    """Test cases for AccessRoleRuleViewSet."""

    def setUp(self):
        """Set up test data."""
        self.superuser = User.objects.create_superuser(
            email='super@test.com',
            password='password',
            first_name='Super',
            last_name='User',
        )
        self.client.force_authenticate(user=self.superuser)
        self.role = Role.objects.create(name='TestRole')
        self.element = BusinessElement.objects.create(name='TestElement')

    def test_list_access_rules(self):
        """Test listing all access rules."""
        AccessRoleRule.objects.create(
            role=self.role, element=self.element, read_permission=True
        )
        url = '/api/rbac/access-rules/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['read_permission'], True)

    def test_create_access_rule(self):
        """Test creating a new access rule."""
        url = '/api/rbac/access-rules/'
        data = {
            'role': str(self.role.id),
            'element': str(self.element.id),
            'read_permission': True,
            'create_permission': False,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['read_permission'], True)
        self.assertEqual(response.data['create_permission'], False)
        self.assertTrue(
            AccessRoleRule.objects.filter(
                role=self.role, element=self.element
            ).exists()
        )

    def test_create_duplicate_access_rule_fails(self):
        """Test that creating duplicate access rule fails."""
        AccessRoleRule.objects.create(
            role=self.role, element=self.element, read_permission=True
        )
        url = '/api/rbac/access-rules/'
        data = {
            'role': str(self.role.id),
            'element': str(self.element.id),
            'create_permission': True,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_access_rule(self):
        """Test retrieving a specific access rule."""
        rule = AccessRoleRule.objects.create(
            role=self.role, element=self.element, read_permission=True
        )
        url = f'/api/rbac/access-rules/{rule.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['read_permission'], True)

    def test_update_access_rule(self):
        """Test updating an access rule."""
        rule = AccessRoleRule.objects.create(
            role=self.role, element=self.element, read_permission=True
        )
        url = f'/api/rbac/access-rules/{rule.id}/'
        data = {
            'role': str(self.role.id),
            'element': str(self.element.id),
            'read_permission': False,
            'create_permission': True,
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['read_permission'], False)
        self.assertEqual(response.data['create_permission'], True)
        rule.refresh_from_db()
        self.assertFalse(rule.read_permission)
        self.assertTrue(rule.create_permission)

    def test_delete_access_rule(self):
        """Test deleting an access rule."""
        rule = AccessRoleRule.objects.create(
            role=self.role, element=self.element, read_permission=True
        )
        url = f'/api/rbac/access-rules/{rule.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(AccessRoleRule.objects.filter(id=rule.id).exists())
