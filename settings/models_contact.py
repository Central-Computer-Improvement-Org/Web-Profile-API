from django.db import models
from common.utils import rename_image_file

class Contact(models.Model):
    id = models.CharField(primary_key=True, max_length=255)

    platform = models.CharField(max_length=255, null=True)
    icon_uri = models.ImageField(upload_to='uploads/contact/')
    value = models.CharField(max_length=255, null=True)
    visited_count = models.IntegerField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self.icon_uri:
            self.icon_uri = rename_image_file(self.icon_uri, prefix="CNT")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.platform