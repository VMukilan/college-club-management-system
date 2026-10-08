"""
Input Validation and Sanitization Module (v0.3 Secure Implementation)
Addresses SEC03: Enforces strict whitelisting, bounds checking, and input
validation.
"""

import re
from datetime import datetime
from .exceptions import ValidationError

DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate_string(value, min_len=1, max_len=255, field_name="Field",
                    min_length=None, max_length=None):
    """
    Validate string presence, length bounds, and strip control characters.
    """
    if min_length is not None:
        min_len = min_length
    if max_length is not None:
        max_len = max_length

    if value is None:
        raise ValidationError(f"{field_name} is required.")

    if not isinstance(value, str):
        raise ValidationError(f"{field_name} must be a valid text string.")

    cleaned = value.strip()
    if len(cleaned) < min_len:
        raise ValidationError(
            f"{field_name} must be at least {min_len} character(s) long."
        )

    if len(cleaned) > max_len:
        raise ValidationError(
            f"{field_name} cannot exceed {max_len} characters."
        )

    # Reject null bytes and non-printable control characters
    if any(ord(c) < 32 and c not in ("\n", "\r", "\t") for c in cleaned):
        raise ValidationError(
            f"{field_name} contains invalid control characters."
        )

    return cleaned


def validate_integer_id(value, field_name="ID"):
    """Validate positive integer ID."""
    if value is None:
        raise ValidationError(f"{field_name} is required.")

    try:
        num = int(value)
    except (ValueError, TypeError, OverflowError):
        raise ValidationError(f"{field_name} must be a valid integer.")

    if num <= 0:
        raise ValidationError(f"{field_name} must be a positive integer.")

    return num


def validate_date_string(value, field_name="Event date"):
    """Validate date format is YYYY-MM-DD and represents a valid date."""
    if not value or not isinstance(value, str):
        raise ValidationError(
            f"{field_name} is required in YYYY-MM-DD format."
        )

    cleaned = value.strip()
    if not DATE_REGEX.match(cleaned):
        raise ValidationError(
            f"{field_name} must match format YYYY-MM-DD (e.g. 2026-12-31)."
        )

    try:
        datetime.strptime(cleaned, "%Y-%m-%d")
    except ValueError:
        raise ValidationError(f"{field_name} is not a valid calendar date.")

    return cleaned
