# Generated by Django 5.0.3 on 2024-05-08 15:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_role_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='division_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.division'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.role'),
        ),
    ]
