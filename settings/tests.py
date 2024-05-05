from django.test import TestCase

from settings.models import Setting, Contact

def _create_setting(id, name, address, telp, description, logo_uri, title_website, keyword):
    Setting.objects.create(id=id, name=name, address=address, telp=telp, description=description, logo_uri=logo_uri, title_website=title_website, keyword=keyword)

def _create_contact(id, platform, icon_uri, value, visited_count):
    Contact.objects.create(id=id, platform=platform, icon_uri=icon_uri, value=value, visited_count=visited_count)

class SettingTestCase(TestCase):

    def setUp(self):
        _create_setting(
            "1", 
            'Central Computer Improvment', 
            'Telkom University, Sukapura, Kabupaten Bandung, Jawa Barat', 
            '082114220492', 
            'Unit Kegiatan Mahasiswa di Telkom University yang berfokus pada bidang ICT (Information, Communication and Technology).', 
            'https://dark-year.info', 
            'CCI', 
            'Test, Test1, Test2'
        )

        _create_contact(
            "1", 
            'Schaden - Hansen',
            'https://dazzling-tofu.net', 
            'http://profitable-century.name',
            0
        )

        _create_contact(
            "2", 
            'Kessler - Jakubowski',
            'https://dazzling-tofuuu.net', 
            'http://profitable-centuryyy.name',
            0
        )
        
    def test_setting_name(self):
        test_setting = Setting.objects.get(id='1')
        self.assertEqual(test_setting.name, "Central Computer Improvment")
        self.assertEqual(test_setting.address, 'Telkom University, Sukapura, Kabupaten Bandung, Jawa Barat')
        self.assertEqual(test_setting.telp, '082114220492')
        self.assertEqual(test_setting.description, 'Unit Kegiatan Mahasiswa di Telkom University yang berfokus pada bidang ICT (Information, Communication and Technology).')
        self.assertEqual(test_setting.logo_uri, 'https://dark-year.info')
        self.assertEqual(test_setting.title_website, 'CCI')
        self.assertEqual(test_setting.keyword, 'Test, Test1, Test2')

    def test_contact_platform(self):
        test_contact = Contact.objects.get(id='1')
        self.assertEqual(test_contact.id, '1')
        self.assertEqual(test_contact.platform, 'Schaden - Hansen')
        self.assertEqual(test_contact.icon_uri, 'https://dazzling-tofu.net')
        self.assertEqual(test_contact.value, 'http://profitable-century.name')
        self.assertEqual(test_contact.visited_count, 0)

        test_contact = Contact.objects.get(id='2')
        self.assertEqual(test_contact.id, '2')
        self.assertEqual(test_contact.platform, 'Kessler - Jakubowski')
        self.assertEqual(test_contact.icon_uri, 'https://dazzling-tofuuu.net')
        self.assertEqual(test_contact.value, 'http://profitable-centuryyy.name')
        self.assertEqual(test_contact.visited_count, 0)



