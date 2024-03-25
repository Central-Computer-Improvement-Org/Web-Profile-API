from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from .models_divisions import Division
from .manager import UserManager
from .models_roles import Role


class User(AbstractBaseUser):
    nim = models.CharField(max_length=255, primary_key=True)
    role_id = models.ForeignKey(Role, on_delete=models.PROTECT)
    division_id = models.ForeignKey(Division, on_delete=models.PROTECT, null=True)
    email = models.EmailField(unique=True)
    major = models.CharField(max_length=255, null=True)
    year_university_enrolled = models.IntegerField(null=True)
    year_community_enrolled = models.IntegerField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nim']

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        permission = self.role_id.permission_id.filter(permission_name=perm)

        if permission:
            return True

    def is_superuser(self):
        return self.role_id.id == 1

    def __str__(self):
        return self.email
