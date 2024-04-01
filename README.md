# CCI Profile Web API

## How to run?

Pastikan python3 dan pip sudah terinstall di komputer!

1. Clone repo ini
2. Buka terminal dan `cd` ke direktori repo ini
3. Jalankan perintah `pip install -r requirements.txt`
4. Setup database mysql
5. Masukkan konfigurasi database ke file `.env` dengan format seperti di bawah
```bash
DATABASE_NAME = "<nama db>"
DATABASE_USER = "<user db>"
DATABASE_PASSWORD = "<password db>"
DATABASE_HOST = "<host db>"
DATABASE_PORT = "<port db>"

JWT_SECRET_KEY="<secret key>" # Buat asal juga boleh
SECRET_KEY="<secret key>" # Buat asal juga boleh
```
6. Migrate database dengan perintah `python manage.py migrate`
7. Buat superuser dengan perintah `python manage.py createsuperuser`
8. Jalankan server dengan perintah `python manage.py runserver`