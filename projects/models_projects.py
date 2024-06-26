from django.db import models

from users.models import Division

from django.core.validators import MinValueValidator

from common.validators import validate_image_size


class Project(models.Model):
    id = models.CharField(primary_key=True, max_length=255)

    name = models.CharField(max_length=255)
    description = models.TextField()
    production_uri = models.CharField(max_length=255)
    repository_uri = models.CharField(max_length=255)
    image_uri = models.ImageField(upload_to="uploads/projects/thumbnails/", validators=[validate_image_size])
    icon_uri = models.ImageField(upload_to="uploads/projects/icons/", validators=[validate_image_size])
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0)])

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    created_by = models.CharField(null=True, max_length=255, default="system")
    updated_by = models.CharField(null=True, max_length=255, default="system")

    def __str__(self):
        return self.platform