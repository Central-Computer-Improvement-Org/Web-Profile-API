from django.db import models

from django.core.validators import MinValueValidator


class Award(models.Model):
    id = models.CharField(primary_key=True, max_length=255)

    issuer = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    created_by = models.CharField(null=True, max_length=255, default="system")
    updated_by = models.CharField(null=True, max_length=255, default="system")

    def __str__(self):
        return self.platform