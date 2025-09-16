"""
Global pytest configuration and fixtures.
"""

import factory
import pytest
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    """DRF API client for testing API endpoints."""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    """API client with authenticated user."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def user():
    """Create a test user."""
    return User.objects.create_user(
        email="test@example.com",
        password="TestPass123!",  # noqa: S106
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def superuser():
    """Create a test superuser."""
    return User.objects.create_superuser(
        email="admin@example.com",
        password="AdminPass123!",  # noqa: S106,
        first_name="Admin",
        last_name="User",
    )


class UserFactory(DjangoModelFactory):
    """Factory for creating test users."""

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True


@pytest.fixture
def user_factory():
    """User factory fixture."""
    return UserFactory
