# Generated by Django 5.0.3 on 2024-05-09 17:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_project_icon_uri_alter_project_image_uri'),
        ('users', '0019_alter_division_logo_uri_alter_user_profile_uri'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='division_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='users.division'),
        ),
    ]
