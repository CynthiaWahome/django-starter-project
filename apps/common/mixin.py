"""
Reusable model and view mixins.
"""

from django.db import models
from django.utils import timezone
from rest_framework import mixins, viewsets

from .responses import APIResponse


class TimestampMixin(models.Model):
    """Add created_at and updated_at timestamps to models."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    """Add soft delete functionality to models."""

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        """Mark as deleted without removing from database."""
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore a soft-deleted object."""
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class StandardizedResponseMixin(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    """Mixin to provide standardized API responses for ViewSets."""

    def list(self, request, *args, **kwargs):
        """Override list to use standardized response."""
        response = super().list(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data, message="Data retrieved successfully"
        )

    def create(self, request, *args, **kwargs):
        """Override create to use standardized response."""
        response = super().create(request, *args, **kwargs)
        return APIResponse.success(
            data=response.data, message="Resource created successfully", status_code=201
        )

    def destroy(self, request, *args, **kwargs):
        """Override destroy to use standardized response."""
        super().destroy(request, *args, **kwargs)
        return APIResponse.success(
            message="Resource deleted successfully", status_code=204
        )
