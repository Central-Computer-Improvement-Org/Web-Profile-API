# Generated by Django 5.0.3 on 2024-05-06 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='active',
        ),
    ]