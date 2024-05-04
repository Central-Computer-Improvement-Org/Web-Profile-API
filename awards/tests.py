# Create your tests here.
from django.test import TestCase

from awards.models_awards import Award
from awards.models_detail_contributor_award import DetailContributorAward

from users.models_roles import Role
from users.models_divisions import Division
from users.models_users import User

def _create_user(nim, role, division, email, phone):
    User.objects.create(nim=nim, role_id=role, division_id=division, email=email, phone_number=phone)


def _create_role(id, role_name):
    Role.objects.create(id=id, name=role_name)


def _create_division(id, division_name, division_description):
    Division.objects.create(id=id, name=division_name, description=division_description)


def _create_award(id, issuer, title, description):
    Award.objects.create(id=id, issuer=issuer, title=title, description=description)


def _create_detail_contributor_award(id, member_nim, award_id):
    DetailContributorAward.objects.create(id=id, member_nim=member_nim, award_id=award_id)


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


        _create_award('1', 'issuer1', 'title1', 'description1')
        _create_award('2', 'issuer2', 'title2', 'description2')
        _create_award('3', 'issuer3', 'title3', 'description3')

        award1 = Award.objects.get(id='1')
        award2 = Award.objects.get(id='2')
        award3 = Award.objects.get(id='3')

        _create_user('1234567890', superuser_role, web_dev_division, 'test1@mail.com', "0896")
        _create_user('1234567891', admin_role, mobile_dev_division, 'test2@mail.com', "0893")
        _create_user('1234567892', user_role, ui_ux_division, 'test3@mail.com', "08977")

        user1 = User.objects.get(id='1234567890')
        user2 = User.objects.get(id='1234567891')
        user3 = User.objects.get(id='1234567892')

        _create_detail_contributor_award('1', user1.id, award1.id)
        _create_detail_contributor_award('2', user2.id, award1.id)
        _create_detail_contributor_award('3', user1.id, award2.id)
        _create_detail_contributor_award('4', user2.id, award2.id)
        _create_detail_contributor_award('5', user3.id, award3.id)
        _create_detail_contributor_award('6', user1.id, award3.id)

    def test_award(self):
        award = Award.objects.get(id='1')
        self.assertEqual(award.title, 'title1')
        self.assertEqual(award.description, 'description1')
        self.assertEqual(award.issuer, 'issuer1')

        award = Award.objects.get(id='2')
        self.assertEqual(award.title, 'title2')

        award = Award.objects.get(id='3')
        self.assertEqual(award.title, 'title3')

    def test_contributor(self):
        contributor = DetailContributorAward.objects.get(id='1')
        self.assertEqual(contributor.member_nim, '1234567890')
        self.assertEqual(contributor.award_id, '1')

        contributor = DetailContributorAward.objects.get(id='2')
        self.assertEqual(contributor.member_nim, '1234567891')
        self.assertEqual(contributor.award_id, '1')

        contributor = DetailContributorAward.objects.get(id='3')
        self.assertEqual(contributor.member_nim, '1234567890')
        self.assertEqual(contributor.award_id, '2')

        contributor = DetailContributorAward.objects.get(id='4')
        self.assertEqual(contributor.member_nim, '1234567891')
        self.assertEqual(contributor.award_id, '2')

        contributor = DetailContributorAward.objects.get(id='5')
        self.assertEqual(contributor.member_nim, '1234567892')
        self.assertEqual(contributor.award_id, '3')

        contributor = DetailContributorAward.objects.get(id='6')
        self.assertEqual(contributor.member_nim, '1234567890')
        self.assertEqual(contributor.award_id, '3')