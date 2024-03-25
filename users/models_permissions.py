from django.db import models


class Permission(models.Model):
    permission_name = models.CharField(max_length=255)
    permission_description = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.permission_name
