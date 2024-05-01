# Create your tests here.
from django.test import TestCase

from projects.models_projects import Project
from projects.models_detail_contributor_project import DetailContributorProject

from users.models_roles import Role
from users.models_divisions import Division
from users.models_users import User

def _create_user(nim, role, division, email, phone):
    User.objects.create(nim=nim, role_id=role, division_id=division, email=email, phone_number=phone)


def _create_role(id, role_name):
    Role.objects.create(id=id, name=role_name)


def _create_division(id, division_name, division_description):
    Division.objects.create(id=id, name=division_name, description=division_description)


def _create_project(id, name, description, production_uri, repository_uri, image_uri, icon_uri, budget):
    Project.objects.create(id=id, name=name, description=description, production_uri=production_uri, repository_uri=repository_uri, image_uri=image_uri, icon_uri=icon_uri, budget=budget)


def _create_detail_contributor_project(id, member_nim, project_id):
    DetailContributorProject.objects.create(id=id, member_nim=member_nim, project_id=project_id)


class ProjectTestCase(TestCase):

    def setUp(self):
        _create_role("SPR", 'Superadmin')
        _create_role("PGR", 'Admin')
        _create_role("USR", 'User')

        superuser_role = Role.objects.get(id='SPR')
        admin_role = Role.objects.get(id='PGR')
        user_role = Role.objects.get(id='USR')

        _create_division("WBD", 'Web Developer', 'Web Developer division')
        _create_division('MBL', 'Mobile Developer division', "Mobile")
        _create_division('DSG', 'UI/UX Designer division', "UI")

        web_dev_division = Division.objects.get(id='WBD')
        mobile_dev_division = Division.objects.get(id='MBL')
        ui_ux_division = Division.objects.get(id='DSG')


        _create_project('1', 'name1', 'description1', 'production_uri1', 'repository_uri1', 'image_uri1', 'icon_uri1', 1000.00)
        _create_project('2', 'name2', 'description2', 'production_uri2', 'repository_uri2', 'image_uri2', 'icon_uri2', 2000.00)
        _create_project('3', 'name3', 'description3', 'production_uri3', 'repository_uri3', 'image_uri3', 'icon_uri3', 3000.00)

        project1 = Project.objects.get(id='1')
        project2 = Project.objects.get(id='2')
        project3 = Project.objects.get(id='3')

        _create_user('1234567890', superuser_role, web_dev_division, 'test1@mail.com', "0896")
        _create_user('1234567891', admin_role, mobile_dev_division, 'test2@mail.com', "0893")
        _create_user('1234567892', user_role, ui_ux_division, 'test3@mail.com', "08977")

        user1 = User.objects.get(id='1234567890')
        user2 = User.objects.get(id='1234567891')
        user3 = User.objects.get(id='1234567892')

        _create_detail_contributor_project('1', user1.id, project1.id)
        _create_detail_contributor_project('2', user2.id, project1.id)
        _create_detail_contributor_project('3', user1.id, project2.id)
        _create_detail_contributor_project('4', user2.id, project2.id)
        _create_detail_contributor_project('5', user3.id, project3.id)
        _create_detail_contributor_project('6', user1.id, project3.id)

    def test_project(self):
        project = Project.objects.get(id='1')
        self.assertEqual(project.title, 'name1')
        self.assertEqual(project.description, 'description1')
        self.assertEqual(project.production_uri, 'production_uri1')

        project = Project.objects.get(id='2')
        self.assertEqual(project.title, 'name2')

        project = Project.objects.get(id='3')
        self.assertEqual(project.title, 'name3')

    def test_contributor(self):
        contributor = DetailContributorProject.objects.get(id='1')
        self.assertEqual(contributor.member_nim, '1234567890')
        self.assertEqual(contributor.project_id, '1')

        contributor = DetailContributorProject.objects.get(id='2')
        self.assertEqual(contributor.member_nim, '1234567891')
        self.assertEqual(contributor.project_id, '1')

        contributor = DetailContributorProject.objects.get(id='3')
        self.assertEqual(contributor.member_nim, '1234567890')
        self.assertEqual(contributor.project_id, '2')

        contributor = DetailContributorProject.objects.get(id='4')
        self.assertEqual(contributor.member_nim, '1234567891')
        self.assertEqual(contributor.project_id, '2')

        contributor = DetailContributorProject.objects.get(id='5')
        self.assertEqual(contributor.member_nim, '1234567892')
        self.assertEqual(contributor.project_id, '3')

        contributor = DetailContributorProject.objects.get(id='6')
        self.assertEqual(contributor.member_nim, '1234567890')
        self.assertEqual(contributor.project_id, '3')