from django.db import models
from django.utils import timezone

from common.validators import validate_image_size

class News(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    media_uri = models.ImageField(upload_to="uploads/news/thumbnails/", validators=[validate_image_size], null=True)

    visited_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    created_by = models.CharField(null=True, max_length=255)
    updated_by = models.CharField(null=True, max_length=255)

    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title
