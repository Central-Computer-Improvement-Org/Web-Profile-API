from django.db import models

class Setting(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, null=True)
    address = models.TextField(null=True)
    telp = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    logo_uri = models.CharField(max_length=255, null=True)
    title_website = models.CharField(max_length=255, null=True)
    keyword = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name