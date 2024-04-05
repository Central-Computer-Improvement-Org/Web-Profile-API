# Generated by Django 5.0.3 on 2024-04-01 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0006_alter_contact_created_at_alter_contact_platform_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='platform',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='value',
            field=models.CharField(max_length=255),
        ),
    ]