from typing import TYPE_CHECKING

from django.contrib.auth import models as base_models

if TYPE_CHECKING:
    from apps.users.models import User  # noqa: F401


class UserManager(base_models.BaseUserManager["User"]):
    def get_queryset(self):
        # Only return users that are not soft-deleted
        return super().get_queryset().filter(is_deleted=False)

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class AllUsersManager(base_models.BaseUserManager):
    def get_queryset(self):
        # Return all users, including soft-deleted
        return super().get_queryset()
