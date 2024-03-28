from django.test import TestCase
from datetime import datetime

from settings.models_settings import Setting

def _create_setting(id, name, address, telp, description, logo_uri, title_website, keyword):
    Setting.objects.create(id=id, name=name, address=address, telp=telp, description=description, logo_uri=logo_uri, title_website=title_website, keyword=keyword)

class SettingTestCase(TestCase):
    id = "STG-" + datetime.now().strftime('%Y%m%d%H%M%S')

    def setUp(self):
        _create_setting(id, 'Central Computer Improvment', 'Telkom University, Sukapura, Kabupaten Bandung, Jawa Barat', '082114220492', 'Unit Kegiatan Mahasiswa di Telkom University yang berfokus pada bidang ICT (Information, Communication and Technology).', 'http.cxxx.com', 'CCI', '1, 2, 3, 4')
        
    def test_setting_name(self):
        test_setting = Setting.objects.get(id=id)
        self.assertEqual(test_setting.name, "Central Computer Improvment")

