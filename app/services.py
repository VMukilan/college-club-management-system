"""
Application Service Layer for College Club Management System (v0.3 Secure)

Security Hardening (v0.3):
- SEC01: Centralized, server-side RBAC enforcement across all domain workflows.
- SEC02: Strict object-level and club-level authorization on events.
- SEC03: Input validation and whitelisting via app.validators.
- SEC04: Sanitized error reporting preventing internal information disclosure.
- SEC05: Comprehensive audit logging for all authentication attempts
         (success and failure), event edits, authorization rejections, etc.
"""

import logging
from werkzeug.security import check_password_hash
from .constants import Role, AuditAction
from .exceptions import ValidationError
from .validators import (
    validate_string, validate_integer_id, validate_date_string
)
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
    """Service handling secure authentication and account status validation."""

    def __init__(self, user_repo=None, audit_repo=None):
        self.user_repo = user_repo or UserRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def authenticate(self, username, password):
        """
        Authenticate user credentials with audit logging on both success and
        failure, and account status validation (SEC05 / Account Hardening).
        """
        if not username or not password:
            return None, "Username and password are required"

        user = self.user_repo.get_by_username(username)
        if not user:
            logger.warning(
                "Authentication failed: Unknown user '%s'", username
            )
            # SEC05 Hardening: Audit failed login attempt
            self.audit_repo.log(
                None,
                AuditAction.LOGIN_FAILURE,
                f"Failed login attempt: Unknown username '{username}'."
            )
            return None, "Invalid username or password"

        # Validate account status (Active vs Suspended)
        if "is_active" in user.keys() and not user["is_active"]:
            logger.warning(
                "Authentication blocked: Inactive user '%s'", username
            )
            self.audit_repo.log(
                user["id"],
                AuditAction.LOGIN_FAILURE,
                f"Login blocked for deactivated account '{username}'."
            )
            return None, "Account is disabled. Contact system administrator."

        if not check_password_hash(user["password_hash"], password):
            logger.warning(
                "Authentication rejected for user '%s'", username
            )
            # SEC05 Hardening: Audit failed password attempt
            self.audit_repo.log(
                user["id"],
                AuditAction.LOGIN_FAILURE,
                f"Failed password verification for user '{username}'."
            )
            return None, "Invalid username or password"

        # SEC05 Hardening: Audit successful login
        self.audit_repo.log(
            user["id"],
            AuditAction.LOGIN_SUCCESS,
            f"User '{username}' authenticated successfully."
        )
        return user, None


class AuthorizationService:
    """
    Centralized Authorization Service (v0.3 Secure Implementation)
    Addresses SEC01: Server-side RBAC permission matrix enforcement.
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
    """Service managing Club domain operations with input validation."""

    def __init__(self, club_repo=None, audit_repo=None):
        self.club_repo = club_repo or ClubRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def get_all_clubs(self):
        return self.club_repo.get_all()

    def get_club_by_id(self, club_id):
        valid_id = validate_integer_id(club_id, "Club ID")
        return self.club_repo.get_by_id(valid_id)

    def create_club(self, name, description, category, admin_user_id):
        # SEC03 Hardening: Input validation and bounds checking
        try:
            val_name = validate_string(name, 3, 50, "Club name")
            val_desc = validate_string(description, 5, 500, "Description")
            val_cat = validate_string(category, 3, 30, "Category")
        except ValidationError as err:
            return False, str(err)

        try:
            club_id = self.club_repo.create(val_name, val_desc, val_cat)
            self.audit_repo.log(
                admin_user_id,
                AuditAction.CLUB_CREATED,
                f"Club '{val_name}' created with ID {club_id}."
            )
            return True, club_id
        except Exception as err:
            logger.error("Club creation failed for '%s': %s", val_name, err)
            return False, "Database error: Unable to create club."


class MembershipService:
    """Service managing Student Club memberships."""

    def __init__(self, membership_repo=None, user_repo=None, audit_repo=None):
        self.membership_repo = membership_repo or MembershipRepository()
        self.user_repo = user_repo or UserRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def join_club(self, user_id, club_id):
        try:
            val_user = validate_integer_id(user_id, "User ID")
            val_club = validate_integer_id(club_id, "Club ID")
        except ValidationError as err:
            return False, str(err)

        if self.membership_repo.exists(val_user, val_club):
            return False, "You are already a member of this club."

        try:
            mem_id = self.membership_repo.add_membership(val_user, val_club)
            self.audit_repo.log(
                val_user,
                AuditAction.CLUB_JOINED,
                f"User #{val_user} joined club ID #{val_club}."
            )
            return True, mem_id
        except Exception as err:
            logger.error("Failed to add membership: %s", err)
            return False, "Unable to join club due to an internal error."

    def get_user_memberships(self, user_id):
        valid_id = validate_integer_id(user_id, "User ID")
        return self.membership_repo.get_user_memberships(valid_id)

    def get_club_members(self, club_id):
        valid_id = validate_integer_id(club_id, "Club ID")
        return self.membership_repo.get_club_members(valid_id)


class EventService:
    """
    Service managing Event scheduling, modification, and queries.
    Enforces Critical Security Scenario (SEC02): Object-level authorization.
    """

    def __init__(self, event_repo=None, announcement_repo=None,
                 audit_repo=None):
        self.event_repo = event_repo or EventRepository()
        self.announcement_repo = announcement_repo or AnnouncementRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def get_all_events(self):
        return self.event_repo.get_all()

    def get_event_by_id(self, event_id):
        valid_id = validate_integer_id(event_id, "Event ID")
        return self.event_repo.get_by_id(valid_id)

    def get_club_events(self, club_id):
        valid_id = validate_integer_id(club_id, "Club ID")
        return self.event_repo.get_by_club(valid_id)

    def _validate_event_payload(self, club_id, title, description,
                                event_date, location):
        """Validate input payload presence and formats (SEC03)."""
        try:
            val_club = validate_integer_id(club_id, "Club ID")
            val_title = validate_string(title, 3, 100, "Event title")
            val_desc = validate_string(
                description, 5, 1000, "Event description"
            )
            val_date = validate_date_string(event_date, "Event date")
            val_loc = validate_string(location, 2, 100, "Location")
            return True, (val_club, val_title, val_desc, val_date, val_loc)
        except ValidationError as err:
            return False, str(err)

    def _publish_event_announcement(self, club_id, title, event_date,
                                    location, user_id):
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
        try:
            self.audit_repo.log(
                user_id,
                AuditAction.EVENT_CREATED,
                f"Created event '{title}' (ID {event_id}) for club #{club_id}."
            )
        except Exception as err:
            logger.warning("Audit logging for event creation failed: %s", err)

    def create_event_with_notifications_and_audit(
        self, club_id, title, description, event_date, location, user_id
    ):
        """Orchestrates secure event creation workflow."""
        is_valid, res = self._validate_event_payload(
            club_id, title, description, event_date, location
        )
        if not is_valid:
            return False, res

        val_club, val_title, val_desc, val_date, val_loc = res

        try:
            event_id = self.event_repo.create(
                club_id=val_club,
                title=val_title,
                description=val_desc,
                event_date=val_date,
                location=val_loc,
                created_by=user_id
            )
        except Exception as err:
            logger.error("Database error creating event: %s", err)
            return False, "Database failure during event creation."

        self._publish_event_announcement(
            val_club, val_title, val_date, val_loc, user_id
        )
        self._log_event_creation(user_id, val_title, event_id, val_club)

        return True, event_id

    def update_event(self, event_id, title, description, event_date, location,
                     user_role, user_id, user_club_id=None):
        """
        Update event details with strict object-level authorization (SEC02).

        CRITICAL SECURITY SCENARIO (v0.3):
        - Coordinator of Club A modifying Club A event -> ALLOW
        - Coordinator of Club A modifying Club B event -> DENY
        - Student modifying event -> DENY
        - Administrator -> ALLOW
        - Audit all modifications and authorization rejections (SEC05).
        """
        # Role verification
        if user_role not in [Role.COORDINATOR, Role.ADMIN]:
            self.audit_repo.log(
                user_id,
                AuditAction.AUTHZ_FAILURE,
                (
                    f"Unauthorized event modification attempt by {user_role} "
                    f"on event #{event_id}."
                )
            )
            return False, (
                "Access Denied: Only coordinators or administrators "
                "can modify events."
            )

        try:
            valid_event_id = validate_integer_id(event_id, "Event ID")
        except ValidationError as err:
            return False, str(err)

        event = self.event_repo.get_by_id(valid_event_id)
        if not event:
            return False, "Event not found"

        # SEC02 CRITICAL SECURITY CONTROL: Object-Level Authorization Check
        if user_role == Role.COORDINATOR:
            if event["club_id"] != user_club_id:
                logger.warning(
                    "SEC02 PREVENTED: Coordinator %s (Club %s) denied "
                    "modifying Event %s (Club %s)",
                    user_id, user_club_id, valid_event_id, event["club_id"]
                )
                self.audit_repo.log(
                    user_id,
                    AuditAction.AUTHZ_FAILURE,
                    (
                        f"Cross-club modification DENIED on event "
                        f"#{valid_event_id} (Club #{event['club_id']}) "
                        f"by Coordinator of Club #{user_club_id}."
                    )
                )
                return False, (
                    "Access Denied: You are not authorized to modify events "
                    "for another club."
                )

        # Input validation (SEC03)
        try:
            val_title = validate_string(title, 3, 100, "Event title")
            val_desc = validate_string(
                description, 5, 1000, "Event description"
            )
            val_date = validate_date_string(event_date, "Event date")
            val_loc = validate_string(location, 2, 100, "Location")
        except ValidationError as err:
            return False, str(err)

        try:
            self.event_repo.update(
                valid_event_id, val_title, val_desc, val_date, val_loc
            )
            # SEC05 Hardening: Audit event modification
            self.audit_repo.log(
                user_id,
                AuditAction.EVENT_MODIFIED,
                (
                    f"Event #{valid_event_id} ('{val_title}') "
                    f"modified by user #{user_id}."
                )
            )
            return True, "Event updated successfully"
        except Exception as err:
            logger.error("Error updating event #%s: %s", valid_event_id, err)
            return False, "Internal error: Failed to update event."


class RegistrationService:
    """Service handling student registrations with validation and audit."""

    def __init__(self, registration_repo=None, audit_repo=None):
        self.registration_repo = registration_repo or RegistrationRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def register_for_event(self, event_id, user_id):
        try:
            val_event = validate_integer_id(event_id, "Event ID")
            val_user = validate_integer_id(user_id, "User ID")
        except ValidationError as err:
            return False, str(err)

        if self.registration_repo.exists(val_event, val_user):
            return False, "You are already registered for this event."

        try:
            reg_id = self.registration_repo.register(val_event, val_user)
            self.audit_repo.log(
                val_user,
                AuditAction.EVENT_REGISTERED,
                f"User #{val_user} registered for event #{val_event}."
            )
            return True, reg_id
        except Exception as err:
            logger.error("Event registration failed: %s", err)
            return False, "Registration failed due to a database error."

    def get_user_registrations(self, user_id):
        valid_id = validate_integer_id(user_id, "User ID")
        return self.registration_repo.get_user_registrations(valid_id)


class AnnouncementService:
    """Service handling campus announcements with club-level validation."""

    def __init__(self, announcement_repo=None, audit_repo=None):
        self.announcement_repo = announcement_repo or AnnouncementRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def get_all_announcements(self):
        return self.announcement_repo.get_all()

    def publish_announcement(self, club_id, title, content, user_id,
                             user_role):
        if user_role not in [Role.COORDINATOR, Role.ADMIN]:
            self.audit_repo.log(
                user_id,
                AuditAction.AUTHZ_FAILURE,
                (
                    f"Unauthorized announcement publish attempt by user "
                    f"#{user_id}."
                )
            )
            return False, "Unauthorized: Coordinator or admin required"

        try:
            val_club = validate_integer_id(club_id, "Club ID")
            val_title = validate_string(title, 3, 100, "Announcement title")
            val_content = validate_string(content, 5, 2000, "Content")
        except ValidationError as err:
            return False, str(err)

        try:
            ann_id = self.announcement_repo.create(
                val_club, val_title, val_content, user_id
            )
            self.audit_repo.log(
                user_id,
                AuditAction.ANNOUNCEMENT_PUBLISHED,
                f"Announcement '{val_title}' published for club #{val_club}."
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
