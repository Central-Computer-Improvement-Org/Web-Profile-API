from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

from .models_divisions import Division
from .manager import UserManager
from .models_roles import Role


class User(AbstractBaseUser):
    nim = models.CharField(max_length=255, primary_key=True)
    role_id = models.ForeignKey(Role, on_delete=models.PROTECT)
    division_id = models.ForeignKey(Division, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    major = models.CharField(max_length=255, null=True)
    linkedin_uri = models.CharField(null=True, max_length=255)
    phone_number = models.CharField(unique=True, max_length=255)
    profile_uri = models.ImageField(upload_to="uploads/user/profile/")

    year_university_enrolled = models.DateField(null=True)
    year_community_enrolled = models.DateField(null=True)

    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True)

    created_by = models.CharField(null=True, max_length=255)
    updated_by = models.CharField(null=True, max_length=255)

    USERNAME_FIELD = 'nim'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def is_superuser(self):
        return self.role_id.name == "Superadmin"

    def is_pengurus(self):
        return self.role_id.name == "Pengurus" or self.role_id.name == "Superadmin"

    def is_member(self):
        return self.role_id.name == "Member" or self.role_id.name == "Pengurus" or self.role_id.name == "Superadmin"

    def is_active(self):
        return self.active

    def __str__(self):
        return self.email
