"""
Application Service Layer for College Club Management System (v0.2 Refactored)

Refactoring Highlights (v0.2):
- CS02: Decomposed long monolithic event creation method into modular helpers.
- CS03: Replaced large nested conditionals in AuthorizationService with a
        declarative permission map.
- CS04: Adopted centralized Role and AuditAction constants.
- CS06: Improved exception handling using logging and structured error
        feedback.
- CS07: Removed dead/unreferenced functions (legacy_calculate_club_score,
        old_fetch_user_by_id).
"""

import logging
from werkzeug.security import check_password_hash
from .constants import Role, AuditAction
from .repositories import (
    UserRepository,
    ClubRepository,
    MembershipRepository,
    EventRepository,
    RegistrationRepository,
    AnnouncementRepository,
    AuditRepository
)

logger = logging.getLogger(__name__)


class AuthenticationService:
    """Service handling user authentication and credential verification."""

    def __init__(self, user_repo=None, audit_repo=None):
        self.user_repo = user_repo or UserRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def authenticate(self, username, password):
        """Authenticate user credentials against hashed password."""
        if not username or not password:
            return None, "Username and password are required"

        user = self.user_repo.get_by_username(username)
        if not user:
            logger.warning(
                "Authentication failed: Unknown user '%s'", username
            )
            return None, "Invalid username or password"

        if not check_password_hash(user["password_hash"], password):
            logger.warning(
                "Authentication rejected for user '%s'",
                username
            )
            return None, "Invalid username or password"

        self.audit_repo.log(
            user["id"],
            AuditAction.LOGIN_SUCCESS,
            f"User {username} authenticated successfully."
        )
        return user, None


class AuthorizationService:
    """
    Authorization Service (v0.2 Refactored)
    Addresses CS03: Uses declarative permission mapping instead of
    deeply nested if-elif statements.
    """

    ROLE_PERMISSIONS = {
        Role.ADMIN: {
            "admin_dashboard": ["view"],
            "club_management": ["create", "edit", "view"],
            "coordinator_management": ["assign", "view"],
            "audit_logs": ["view"],
            "events": ["create", "edit", "view"],
            "announcements": ["create", "view"],
            "clubs": ["create", "edit", "view"],
            "members": ["view", "manage"],
        },
        Role.COORDINATOR: {
            "events": ["create", "edit", "view"],
            "announcements": ["create", "view"],
            "members": ["view", "manage"],
            "clubs": ["view"],
        },
        Role.STUDENT: {
            "events": ["view", "register"],
            "announcements": ["view"],
            "clubs": ["view", "join"],
        },
    }

    def check_access(self, role, required_resource, action="view"):
        """Check if role has permission for given resource and action."""
        if role not in self.ROLE_PERMISSIONS:
            return False

        resource_permissions = self.ROLE_PERMISSIONS[role].get(
            required_resource, []
        )
        return action in resource_permissions


class ClubService:
    """Service managing Club domain operations."""

    def __init__(self, club_repo=None, audit_repo=None):
        self.club_repo = club_repo or ClubRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def get_all_clubs(self):
        return self.club_repo.get_all()

    def get_club_by_id(self, club_id):
        return self.club_repo.get_by_id(club_id)

    def create_club(self, name, description, category, admin_user_id):
        if not name or not description or not category:
            return False, "All club fields are required"

        try:
            club_id = self.club_repo.create(name, description, category)
            self.audit_repo.log(
                admin_user_id,
                AuditAction.CLUB_CREATED,
                f"Club '{name}' created with ID {club_id}."
            )
            return True, club_id
        except Exception as err:
            logger.error("Club creation failed for '%s': %s", name, err)
            return False, "Database error: Unable to create club."


class MembershipService:
    """Service managing Student Club memberships."""

    def __init__(self, membership_repo=None, user_repo=None, audit_repo=None):
        self.membership_repo = membership_repo or MembershipRepository()
        self.user_repo = user_repo or UserRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def join_club(self, user_id, club_id):
        if self.membership_repo.exists(user_id, club_id):
            return False, "You are already a member of this club."

        try:
            mem_id = self.membership_repo.add_membership(user_id, club_id)
            self.audit_repo.log(
                user_id,
                AuditAction.CLUB_JOINED,
                f"User joined club ID {club_id}."
            )
            return True, mem_id
        except Exception as err:
            logger.error("Failed to add membership: %s", err)
            return False, "Unable to join club due to an internal error."

    def get_user_memberships(self, user_id):
        return self.membership_repo.get_user_memberships(user_id)

    def get_club_members(self, club_id):
        return self.membership_repo.get_club_members(club_id)


class EventService:
    """Service managing Event scheduling, modification, and queries."""

    def __init__(self, event_repo=None, announcement_repo=None,
                 audit_repo=None):
        self.event_repo = event_repo or EventRepository()
        self.announcement_repo = announcement_repo or AnnouncementRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def get_all_events(self):
        return self.event_repo.get_all()

    def get_event_by_id(self, event_id):
        return self.event_repo.get_by_id(event_id)

    def get_club_events(self, club_id):
        return self.event_repo.get_by_club(club_id)

    # CS02 Refactoring: Decomposed long monolithic method into focused helpers
    def _validate_event_payload(self, club_id, title, description,
                                event_date, location):
        """Validate input payload presence (CS02 sub-method)."""
        if not club_id:
            return False, "Club ID is required"
        if not title:
            return False, "Event title is required"
        if not description:
            return False, "Event description is required"
        if not event_date:
            return False, "Event date is required"
        if not location:
            return False, "Location is required"
        return True, None

    def _publish_event_announcement(self, club_id, title, event_date,
                                    location, user_id):
        """Publish automatic notification for newly created event (CS02)."""
        ann_title = f"New Event: {title}"
        ann_content = (
            f"An event '{title}' has been scheduled for {event_date} "
            f"at {location}. Join us!"
        )
        try:
            self.announcement_repo.create(
                club_id=club_id,
                title=ann_title,
                content=ann_content,
                created_by=user_id
            )
        except Exception as err:
            logger.warning(
                "Could not publish automatic event announcement: %s", err
            )

    def _log_event_creation(self, user_id, title, event_id, club_id):
        """Record audit log entry for event creation (CS02)."""
        try:
            self.audit_repo.log(
                user_id,
                AuditAction.EVENT_CREATED,
                f"Created event '{title}' (ID {event_id}) for club {club_id}."
            )
        except Exception as err:
            logger.warning("Audit logging for event creation failed: %s", err)

    def create_event_with_notifications_and_audit(
        self, club_id, title, description, event_date, location, user_id
    ):
        """
        Orchestrates event creation workflow (CS02 decomposed).
        """
        is_valid, validation_msg = self._validate_event_payload(
            club_id, title, description, event_date, location
        )
        if not is_valid:
            return False, validation_msg

        fmt_title = title.strip()
        fmt_desc = description.strip()
        fmt_loc = location.strip()

        try:
            event_id = self.event_repo.create(
                club_id=club_id,
                title=fmt_title,
                description=fmt_desc,
                event_date=event_date,
                location=fmt_loc,
                created_by=user_id
            )
        except Exception as err:
            logger.error("Database error creating event: %s", err)
            return False, "Database failure during event creation."

        self._publish_event_announcement(
            club_id, fmt_title, event_date, fmt_loc, user_id
        )
        self._log_event_creation(user_id, fmt_title, event_id, club_id)

        return True, event_id

    def update_event(self, event_id, title, description, event_date, location,
                     user_role, user_club_id=None):
        """
        Update event details.
        Note: Controlled security weakness SEC02 remains intentionally intact
        in v0.2 until v0.3 security hardening.
        """
        if user_role not in [Role.COORDINATOR, Role.ADMIN]:
            return False, "Unauthorized: Requires coordinator or admin role"

        event = self.event_repo.get_by_id(event_id)
        if not event:
            return False, "Event not found"

        try:
            self.event_repo.update(
                event_id, title, description, event_date, location
            )
            return True, "Event updated successfully"
        except Exception as err:
            logger.error("Error updating event #%s: %s", event_id, err)
            return False, "Internal error: Failed to update event."


class RegistrationService:
    """Service handling student event registrations."""

    def __init__(self, registration_repo=None, audit_repo=None):
        self.registration_repo = registration_repo or RegistrationRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def register_for_event(self, event_id, user_id):
        if self.registration_repo.exists(event_id, user_id):
            return False, "You are already registered for this event."

        try:
            reg_id = self.registration_repo.register(event_id, user_id)
            self.audit_repo.log(
                user_id,
                AuditAction.EVENT_REGISTERED,
                f"User registered for event ID {event_id}."
            )
            return True, reg_id
        except Exception as err:
            logger.error("Event registration failed: %s", err)
            return False, "Registration failed due to a database error."

    def get_user_registrations(self, user_id):
        return self.registration_repo.get_user_registrations(user_id)


class AnnouncementService:
    """Service handling campus announcements."""

    def __init__(self, announcement_repo=None, audit_repo=None):
        self.announcement_repo = announcement_repo or AnnouncementRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def get_all_announcements(self):
        return self.announcement_repo.get_all()

    def publish_announcement(self, club_id, title, content, user_id,
                             user_role):
        if user_role not in [Role.COORDINATOR, Role.ADMIN]:
            return False, "Unauthorized: Coordinator or admin required"

        if not title or not content:
            return False, "Title and content cannot be blank"

        try:
            ann_id = self.announcement_repo.create(
                club_id, title, content, user_id
            )
            self.audit_repo.log(
                user_id,
                AuditAction.ANNOUNCEMENT_PUBLISHED,
                f"Announcement '{title}' published."
            )
            return True, ann_id
        except Exception as err:
            logger.error("Announcement publication failed: %s", err)
            return False, "Failed to publish announcement."


class AuditService:
    """Service managing audit trail inspection."""

    def __init__(self, audit_repo=None):
        self.audit_repo = audit_repo or AuditRepository()

    def get_audit_trail(self, user_role):
        if user_role != Role.ADMIN:
            return []
        return self.audit_repo.get_all()
