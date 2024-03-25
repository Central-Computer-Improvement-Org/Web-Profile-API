from django.db import models

from users.models_permissions import Permission


class Role(models.Model):
    role_name = models.CharField(max_length=255)
    role_description = models.CharField(max_length=255)
    permission_id = models.ManyToManyField(Permission)

    def __str__(self):
        return self.role_name


