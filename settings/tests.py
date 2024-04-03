from django.test import TestCase
from datetime import datetime

from settings.models_settings import Setting

def _create_setting(id, name, address, telp, description, logo_uri, title_website, keyword):
    Setting.objects.create(id=id, name=name, address=address, telp=telp, description=description, logo_uri=logo_uri, title_website=title_website, keyword=keyword)

def _create_contact(id, platform, icon_uri, value, visited_count):
    Setting.objects.create(id=id, platform=platform, icon_uri=icon_uri, value=value, visited_count=visited_count)

class SettingTestCase(TestCase):
    id_setting = "STG-" + datetime.now().strftime('%Y%m%d%H%M%S')
    id_contact = "CNT-" + datetime.now().strftime('%Y%m%d%H%M%S')

    def setUp(self):
        _create_setting(
            id_setting, 
            'Central Computer Improvment', 
            'Telkom University, Sukapura, Kabupaten Bandung, Jawa Barat', 
            '082114220492', 
            'Unit Kegiatan Mahasiswa di Telkom University yang berfokus pada bidang ICT (Information, Communication and Technology).', 
            'http://127.0.0.1:8000/uploads/setting/test.png', 
            'CCI', 
            '1, 2, 3, 4'
        )

        _create_contact(
            id_contact, 
            'facebook',
            'http://127.0.0.1:8000/uploads/setting/test.png', 
            'http://profitable-century.name',
            0
        )
        
    def test_setting_name(self):
        test_setting = Setting.objects.get(id=id)
        self.assertEqual(test_setting.name, "Central Computer Improvment")

    def test_contact_platform(self):
        test_contact = Contact.objects.get(id=id)
        self.assertEqual(test_contact.platform, "facebook")

