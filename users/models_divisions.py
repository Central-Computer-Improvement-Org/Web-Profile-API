from django.db import models
from django.utils import timezone

from common.validators import validate_image_size


class Division(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    logo_uri = models.ImageField(upload_to="uploads/divisions/logo/", null=True, validators=[validate_image_size])

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    created_by = models.CharField(null=True, max_length=255, default="system")
    updated_by = models.CharField(null=True, max_length=255, default="system")

    def __str__(self) -> str:
        return self.name
