from django.contrib.auth import models as base_models
from django.db import models
from django.utils import timezone

from apps.common.mixin import SoftDeleteMixin, TimestampMixin
from apps.users import managers


class User(
    base_models.AbstractBaseUser,
    base_models.PermissionsMixin,
    TimestampMixin,
    SoftDeleteMixin,
):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    objects = managers.UserManager()  # Default manager
    all_objects = managers.AllUsersManager()  # Manager to include soft-deleted users

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def get_username(self):
        return self.email


class Group(base_models.Group):
    class Meta:
        proxy = True
