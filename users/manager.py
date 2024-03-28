from django.contrib.auth.base_user import BaseUserManager

from returns.result import Result

from users.models_roles import Role


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields) -> Result['User', Exception]:
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields) -> Result['User', Exception]:
        role = Role.objects.get(id="SPR")
        extra_fields.setdefault('role_id', role)
        return self.create_user(email, password, **extra_fields)
