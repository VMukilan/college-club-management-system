"""
Custom Domain Exceptions (v0.2 Refactored)
Addresses CS06: Replaces generic exception swallowing with explicit
domain exceptions.
"""


class ClubAppException(Exception):
    """Base exception for College Club Management System."""

    def __init__(self, message="An internal application error occurred."):
        super().__init__(message)
        self.message = message


class ValidationError(ClubAppException):
    """Raised when user input fails validation constraints."""
    pass


class AuthenticationError(ClubAppException):
    """Raised when authentication credentials fail verification."""
    pass


class AuthorizationError(ClubAppException):
    """Raised when user lacks required permissions for an operation."""
    pass


class ResourceNotFoundError(ClubAppException):
    """Raised when a requested entity does not exist."""
    pass


class DatabaseOperationError(ClubAppException):
    """Raised when an underlying database interaction fails."""
    pass
