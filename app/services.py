"""
Application Service Layer for College Club Management System (v0.1)

Contains:
- Authentication Service
- Authorization Service
- Club Service
- Membership Service
- Event Service
- Registration Service
- Announcement Service
- Audit Service

Controlled Code Smells:
- CS01: Duplicated auth/role checking logic
- CS02: Long method (create_event_with_notifications_and_audit)
- CS03: Large conditionals / excessive role checking
- CS04: Hard-coded role strings and configuration values
- CS05: Duplicated database connection logic
- CS06: Poor exception handling (swallowing errors or returning raw traces)
- CS07: Unused/dead code functions

Controlled Security Weaknesses:
- SEC01: Non-centralized authorization checks
- SEC02: Event modification does not verify coordinator club association (IDOR)
- SEC03: Incomplete input validation
- SEC04: Raw exception messages exposed in errors
- SEC05: Missing audit logs for sensitive operations (failed auth, event edits)
"""

import sqlite3
from flask import current_app
from werkzeug.security import check_password_hash
from .repositories import (
    UserRepository,
    ClubRepository,
    MembershipRepository,
    EventRepository,
    RegistrationRepository,
    AnnouncementRepository,
    AuditRepository
)


# CS07: Dead / Unused code - Legacy functions left behind
def legacy_calculate_club_score(club_id):
    """Deprecated function from early prototype - not used anywhere in v0.1."""
    score = 100
    multiplier = 1.5
    return (score * multiplier) + club_id


def old_fetch_user_by_id(user_id):
    """Old database retrieval function that was replaced by UserRepository."""
    # CS05: Duplicated direct DB connection logic
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = " + str(user_id))
    row = cur.fetchone()
    conn.close()
    return row


class AuthenticationService:
    def __init__(self, user_repo=None, audit_repo=None):
        self.user_repo = user_repo or UserRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def authenticate(self, username, password):
        """
        Authenticate user by username and password.
        SEC05: Failed logins are NOT audited in v0.1!
        """
        if not username or not password:
            return None, "Username and password are required"

        user = self.user_repo.get_by_username(username)
        if not user:
            # SEC05: Missing audit log for failed login attempt
            return None, "Invalid username or password"

        if not check_password_hash(user['password_hash'], password):
            # SEC05: Missing audit log for failed login attempt
            return None, "Invalid username or password"

        # Log successful login to audit
        self.audit_repo.log(user['id'], "LOGIN_SUCCESS", f"User {username} logged in successfully.")
        return user, None


class AuthorizationService:
    """
    Authorization Service (v0.1)
    SEC01: Ad-hoc authorization logic without central decorator enforcement.
    CS03: Large conditionals with excessive role checks.
    CS04: Hardcoded role string literals ('admin', 'coordinator', 'student').
    """
    def __init__(self):
        pass

    def check_access(self, role, required_resource, action="view"):
        # CS03: Large conditional block with multiple nested role comparisons
        if role == "admin":
            if required_resource == "admin_dashboard":
                return True
            elif required_resource == "club_management":
                return True
            elif required_resource == "coordinator_management":
                return True
            elif required_resource == "audit_logs":
                return True
            elif required_resource == "events":
                return True
            elif required_resource == "announcements":
                return True
            else:
                return True
        elif role == "coordinator":
            if required_resource == "admin_dashboard":
                return False
            elif required_resource == "coordinator_management":
                return False
            elif required_resource == "events" and action in ["create", "edit", "view"]:
                return True
            elif required_resource == "announcements" and action in ["create", "view"]:
                return True
            elif required_resource == "members" and action in ["view", "manage"]:
                return True
            elif required_resource == "clubs" and action == "view":
                return True
            else:
                return False
        elif role == "student":
            if required_resource == "admin_dashboard" or required_resource == "coordinator_management":
                return False
            elif required_resource == "events" and action in ["view", "register"]:
                return True
            elif required_resource == "announcements" and action == "view":
                return True
            elif required_resource == "clubs" and action in ["view", "join"]:
                return True
            else:
                return False
        else:
            return False


class ClubService:
    def __init__(self, club_repo=None, audit_repo=None):
        self.club_repo = club_repo or ClubRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def get_all_clubs(self):
        return self.club_repo.get_all()

    def get_club_by_id(self, club_id):
        return self.club_repo.get_by_id(club_id)

    def create_club(self, name, description, category, admin_user_id):
        # SEC03: Incomplete input validation (no length check or regex)
        if not name or not description or not category:
            return False, "All club fields are required"

        try:
            club_id = self.club_repo.create(name, description, category)
            self.audit_repo.log(admin_user_id, "CLUB_CREATED", f"Club '{name}' created with ID {club_id}.")
            return True, club_id
        except Exception as e:
            # CS06 & SEC04: Exposure of internal exception details
            return False, f"Database error creating club: {str(e)}"


class MembershipService:
    def __init__(self, membership_repo=None, user_repo=None, audit_repo=None):
        self.membership_repo = membership_repo or MembershipRepository()
        self.user_repo = user_repo or UserRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def join_club(self, user_id, club_id):
        if self.membership_repo.exists(user_id, club_id):
            return False, "You are already a member of this club."

        try:
            mem_id = self.membership_repo.add_membership(user_id, club_id)
            self.audit_repo.log(user_id, "CLUB_JOINED", f"User joined club ID {club_id}.")
            return True, mem_id
        except Exception as e:
            # CS06 & SEC04: Poor exception handling and raw error exposure
            return False, f"Failed to join club: {str(e)}"

    def get_user_memberships(self, user_id):
        return self.membership_repo.get_user_memberships(user_id)

    def get_club_members(self, club_id):
        return self.membership_repo.get_club_members(club_id)


class EventService:
    def __init__(self, event_repo=None, announcement_repo=None, audit_repo=None):
        self.event_repo = event_repo or EventRepository()
        self.announcement_repo = announcement_repo or AnnouncementRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def get_all_events(self):
        return self.event_repo.get_all()

    def get_event_by_id(self, event_id):
        return self.event_repo.get_by_id(event_id)

    def get_club_events(self, club_id):
        return self.event_repo.get_by_club(club_id)

    # CS02: Long Method smell (> 60 lines of combined logic, multi-purpose responsibility)
    def create_event_with_notifications_and_audit(self, club_id, title, description, event_date, location, user_id):
        """
        CS02: Monolithic method handling validation, formatting, event creation,
        automatic announcement creation, audit logging, and debug outputs.
        """
        # Step 1: Input presence check (SEC03: basic presence only, no format sanitization)
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

        # Step 2: Format strings and sanitize loosely
        formatted_title = title.strip()
        formatted_desc = description.strip()
        formatted_loc = location.strip()

        # Step 3: Insert Event into database
        try:
            event_id = self.event_repo.create(
                club_id=club_id,
                title=formatted_title,
                description=formatted_desc,
                event_date=event_date,
                location=formatted_loc,
                created_by=user_id
            )
        except Exception as e:
            # SEC04 & CS06: Leaking DB error
            return False, f"Database failure during event creation: {str(e)}"

        # Step 4: Automatically publish an associated announcement
        announcement_title = f"New Event: {formatted_title}"
        announcement_content = f"An event '{formatted_title}' has been scheduled for {event_date} at {formatted_loc}. Join us!"
        try:
            self.announcement_repo.create(
                club_id=club_id,
                title=announcement_title,
                content=announcement_content,
                created_by=user_id
            )
        except Exception:
            # CS06: Silent exception swallowing
            pass

        # Step 5: Audit log entry
        try:
            self.audit_repo.log(
                user_id,
                "EVENT_CREATED",
                f"Created event '{formatted_title}' (ID {event_id}) for club {club_id}."
            )
        except Exception:
            # CS06: Silent exception swallowing
            pass

        return True, event_id

    def update_event(self, event_id, title, description, event_date, location, user_role, user_club_id=None):
        """
        Update event details.
        SEC02: Controlled Security Weakness!
        It checks that the user has role 'coordinator' or 'admin', but it does NOT verify
        that the coordinator's assigned club matches the event's club!
        A coordinator from Club 1 can modify Club 2's event!
        SEC05: Does NOT record an audit log for event modifications in v0.1!
        """
        # CS01 & CS04: Inconsistent authorization check
        if user_role not in ["coordinator", "admin"]:
            return False, "Unauthorized: Only coordinators or admins can modify events"

        event = self.event_repo.get_by_id(event_id)
        if not event:
            return False, "Event not found"

        # SEC02 VULNERABILITY:
        # In v0.1, the check `if user_role == 'coordinator' and event['club_id'] != user_club_id`
        # is INTENTIONALLY OMITTED to demonstrate SEC02 (unauthorized event modification).

        try:
            self.event_repo.update(event_id, title, description, event_date, location)
            # SEC05 VULNERABILITY: No audit log written for event modification!
            return True, "Event updated successfully"
        except Exception as e:
            # SEC04: Exposing exception message
            return False, f"Error updating event: {str(e)}"


class RegistrationService:
    def __init__(self, registration_repo=None, audit_repo=None):
        self.registration_repo = registration_repo or RegistrationRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def register_for_event(self, event_id, user_id):
        if self.registration_repo.exists(event_id, user_id):
            return False, "You are already registered for this event."

        try:
            reg_id = self.registration_repo.register(event_id, user_id)
            self.audit_repo.log(user_id, "EVENT_REGISTERED", f"User registered for event ID {event_id}.")
            return True, reg_id
        except Exception as e:
            # SEC04 & CS06: Internal trace exposed
            return False, f"Registration failed: {str(e)}"

    def get_user_registrations(self, user_id):
        return self.registration_repo.get_user_registrations(user_id)


class AnnouncementService:
    def __init__(self, announcement_repo=None, audit_repo=None):
        self.announcement_repo = announcement_repo or AnnouncementRepository()
        self.audit_repo = audit_repo or AuditRepository()

    def get_all_announcements(self):
        return self.announcement_repo.get_all()

    def publish_announcement(self, club_id, title, content, user_id, user_role):
        # CS01: Ad-hoc authorization check
        if user_role not in ["coordinator", "admin"]:
            return False, "Unauthorized: Only coordinators and administrators can publish announcements"

        # SEC03: Incomplete input validation
        if not title or not content:
            return False, "Title and content cannot be blank"

        try:
            ann_id = self.announcement_repo.create(club_id, title, content, user_id)
            self.audit_repo.log(user_id, "ANNOUNCEMENT_PUBLISHED", f"Announcement '{title}' published.")
            return True, ann_id
        except Exception as e:
            return False, f"Failed to publish announcement: {str(e)}"


class AuditService:
    def __init__(self, audit_repo=None):
        self.audit_repo = audit_repo or AuditRepository()

    def get_audit_trail(self, user_role):
        # CS01 & CS04: Ad-hoc role check
        if user_role != "admin":
            return []
        return self.audit_repo.get_all()
