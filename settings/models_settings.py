from django.db import models
from common.utils import rename_image_file

class Setting(models.Model):
    id = models.CharField(max_length=255, primary_key=True)

    name = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    telp = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    logo_uri = models.ImageField(upload_to='uploads/setting/')
    title_website = models.CharField(max_length=255, null=True)
    keyword = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if self.logo_uri:
            self.logo_uri = rename_image_file(self.logo_uri, prefix="STG")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name