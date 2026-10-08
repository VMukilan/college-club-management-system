"""
Application Constants and Role Definitions (v0.2 Refactored)
Addresses CS04: Centralizes hard-coded configuration and domain strings.
"""


class Role:
    """User role identifiers."""
    ADMIN = "admin"
    COORDINATOR = "coordinator"
    STUDENT = "student"

    ALL_ROLES = [ADMIN, COORDINATOR, STUDENT]


class MembershipStatus:
    """Club membership lifecycle statuses."""
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    REVOKED = "REVOKED"


class RegistrationStatus:
    """Event registration statuses."""
    REGISTERED = "REGISTERED"
    CANCELLED = "CANCELLED"


class AuditAction:
    """Standardized action tags for audit logging."""
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGIN_FAILURE = "LOGIN_FAILURE"
    SYSTEM_INIT = "SYSTEM_INIT"
    CLUB_CREATED = "CLUB_CREATED"
    CLUB_JOINED = "CLUB_JOINED"
    EVENT_CREATED = "EVENT_CREATED"
    EVENT_MODIFIED = "EVENT_MODIFIED"
    EVENT_REGISTERED = "EVENT_REGISTERED"
    ANNOUNCEMENT_PUBLISHED = "ANNOUNCEMENT_PUBLISHED"
    COORDINATOR_ASSIGNED = "COORDINATOR_ASSIGNED"
