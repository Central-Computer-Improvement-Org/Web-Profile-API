from django.contrib.auth.hashers import make_password

import os
import sys

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cci_rebuild_be.settings')

import django
django.setup()

password = sys.argv[1]

print(make_password(password))
