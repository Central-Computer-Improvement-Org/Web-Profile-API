# Generated by Django 5.0.3 on 2024-04-05 18:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_project_budget'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DetailContributorProject',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('created_by', models.CharField(default='system', max_length=255, null=True)),
                ('updated_by', models.CharField(default='system', max_length=255, null=True)),
                ('member_nim', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projects.project')),
            ],
        ),
    ]
