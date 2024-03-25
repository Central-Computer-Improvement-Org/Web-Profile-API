from django.db import models


class Division(models.Model):
    division_name = models.CharField(max_length=255)
    division_description = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.division_name
