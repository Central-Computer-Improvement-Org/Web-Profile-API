from django.db import models

from users.models_divisions import Division

from common.validators import validate_image_size


# Create your models here.

class Event(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=130)
    division_id = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True)
    media_uri = models.ImageField(upload_to="uploads/events/thumbnails/", validators=[validate_image_size])
    held_on = models.DateField()
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    created_by = models.CharField(null=True, max_length=255)
    updated_by = models.CharField(null=True, max_length=255)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name