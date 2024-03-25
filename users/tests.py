from django.test import TestCase

from users.models_roles import Role
from users.models_permissions import Permission
from users.models_divisions import Division
from users.models_users import User


def _add_permission(role: Role, permission: Permission):
    role.permission_id.add(permission)


def _create_user(nim, role, division, email):
    User.objects.create(nim=nim, role_id=role, division_id=division, email=email)


def _create_permission(permission_name, permission_description):
    Permission.objects.create(permission_name=permission_name, permission_description=permission_description)


def _create_role(id, role_name, role_description):
    Role.objects.create(id=id, role_name=role_name, role_description=role_description)


def _create_division(division_name, division_description):
    Division.objects.create(division_name=division_name, division_description=division_description)


class UserTestCase(TestCase):

    def setUp(self):
        _create_permission('Create', 'Create permission')
        _create_permission('Read', 'Read permission')
        _create_permission('Update', 'Update permission')
        _create_permission('Delete', 'Delete permission')

        create_perm = Permission.objects.get(permission_name='Create')
        read_perm = Permission.objects.get(permission_name='Read')
        update_perm = Permission.objects.get(permission_name='Update')
        delete_perm = Permission.objects.get(permission_name='Delete')

        _create_role(1, 'Superuser', 'Superuser role')
        _create_role(2, 'Admin', 'Admin role')
        _create_role(3, 'User', 'User role')

        superuser_role = Role.objects.get(role_name='Superuser')
        admin_role = Role.objects.get(role_name='Admin')
        user_role = Role.objects.get(role_name='User')

        _add_permission(superuser_role, create_perm)
        _add_permission(superuser_role, read_perm)
        _add_permission(superuser_role, update_perm)
        _add_permission(superuser_role, delete_perm)

        _add_permission(admin_role, read_perm)
        _add_permission(admin_role, update_perm)

        _add_permission(user_role, read_perm)

        _create_division('Web Developer', 'Web Developer division')
        _create_division('Mobile Developer', 'Mobile Developer division')
        _create_division('UI/UX Designer', 'UI/UX Designer division')

        web_dev_division = Division.objects.get(division_name='Web Developer')
        mobile_dev_division = Division.objects.get(division_name='Mobile Developer')
        ui_ux_division = Division.objects.get(division_name='UI/UX Designer')

        _create_user('1234567890', superuser_role, web_dev_division, 'test1@mail.com')
        _create_user('1234567891', admin_role, mobile_dev_division, 'test2@mail.com')
        _create_user('1234567892', user_role, ui_ux_division, 'test3@mail.com')

    def test_user_role(self):
        test_user = User.objects.get(nim='1234567890')
        self.assertEqual(test_user.role_id.role_name, 'Superuser')

    def test_user_division(self):
        test_user = User.objects.get(nim='1234567890')
        self.assertEqual(test_user.division_id.division_name, 'Web Developer')

    def test_user_permission(self):
        test_user = User.objects.get(nim='1234567890')
        self.assertEqual(test_user.has_perm('Create'), True)
        self.assertEqual(test_user.has_perm('Read'), True)
        self.assertEqual(test_user.has_perm('Update'), True)
        self.assertEqual(test_user.has_perm('Delete'), True)

    def test_user_superuser(self):
        test_user = User.objects.get(nim='1234567890')
        self.assertEqual(test_user.is_superuser(), True)
