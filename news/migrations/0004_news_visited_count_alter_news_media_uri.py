# Generated by Django 5.0.3 on 2024-05-09 14:53

import common.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_detailnewsmedia_media_uri_alter_news_media_uri'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='visited_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='news',
            name='media_uri',
            field=models.ImageField(null=True, upload_to='uploads/news/thumbnails/', validators=[common.validators.validate_image_size]),
        ),
    ]
