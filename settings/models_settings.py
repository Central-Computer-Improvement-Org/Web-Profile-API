from django.db import models

class Setting(models.Model):
    id = models.CharField(max_length=255, primary_key=True)

    name = models.CharField(max_length=255)
    address = models.TextField()
    telp = models.CharField(max_length=255)
    description = models.TextField(max_length=255)

    logo_uri = models.ImageField(upload_to='uploads/setting/')
    title_website = models.CharField(max_length=255)
    keyword = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    created_by = models.CharField(null=True, max_length=255, default="system")
    updated_by = models.CharField(null=True, max_length=255, default="system")

    def __str__(self):
        return self.name