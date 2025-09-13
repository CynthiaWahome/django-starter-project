"""
Custom validators for user-related fields and files.
"""
import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


def validate_strong_password(password: str) -> None:
    """Validate password strength with clear requirements."""
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter.")

    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter.")

    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit.")

    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\?]', password):
        errors.append("Password must contain at least one special character.")

    if errors:
        raise ValidationError(errors)


def validate_email_and_password(email, password):
    """
    Validate that the email and password match an existing user.

    Raises a standardized error if not.
    """
    from apps.users.models import User

    email = email.lower().strip()
    try:
        user = User.all_objects.get(email=email)
    except User.DoesNotExist as e:
        raise ValidationError("Invalid email, phone number, or password.") from e

    if not user.check_password(password):
        raise ValidationError("Invalid email, phone number, or password.")

    return user


def validate_password_strength(password, min_length=8):
    """Enforce password strength requirements."""
    if len(password) < min_length:
        raise ValidationError(f"Password must be at least {min_length} characters long.")

    if not re.search(r"[A-Za-z]", password):
        raise ValidationError("Password must contain at least one letter.")

    if not re.search(r"\d", password):
        raise ValidationError("Password must contain at least one digit.")

    return password
