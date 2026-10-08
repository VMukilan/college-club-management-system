"""
Repository Layer for College Club Management System (v0.2 Refactored)
Provides data access methods for domain entities using the Repository Pattern.
Addresses CS05: Consolidates all database operations inside repositories.
"""

from .database import get_db


class UserRepository:
    """Repository handling User entity persistence and retrieval."""

    def __init__(self, db=None):
        self.db = db

    def _get_conn(self):
        return self.db if self.db is not None else get_db()

    def get_by_id(self, user_id):
        cursor = self._get_conn().cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        return cursor.fetchone()

    def get_by_username(self, username):
        cursor = self._get_conn().cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        )
        return cursor.fetchone()

    def get_all(self):
        cursor = self._get_conn().cursor()
        cursor.execute("SELECT * FROM users ORDER BY id ASC")
        return cursor.fetchall()

    def get_coordinators(self):
        cursor = self._get_conn().cursor()
        cursor.execute(
            "SELECT * FROM users WHERE role = 'coordinator' ORDER BY id ASC"
        )
        return cursor.fetchall()

    def update_coordinator_club(self, user_id, club_id):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET club_id = ? WHERE id = ?",
            (club_id, user_id)
        )
        conn.commit()


class ClubRepository:
    """Repository handling Club entity persistence and metrics."""

    def __init__(self, db=None):
        self.db = db

    def _get_conn(self):
        return self.db if self.db is not None else get_db()

    def count(self):
        """Return total count of registered clubs (CS05 centralization)."""
        cursor = self._get_conn().cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM clubs")
        row = cursor.fetchone()
        return row["total"] if row else 0

    def get_all(self):
        cursor = self._get_conn().cursor()
        cursor.execute("SELECT * FROM clubs ORDER BY name ASC")
        return cursor.fetchall()

    def get_by_id(self, club_id):
        cursor = self._get_conn().cursor()
        cursor.execute("SELECT * FROM clubs WHERE id = ?", (club_id,))
        return cursor.fetchone()

    def create(self, name, description, category):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO clubs (name, description, category)
            VALUES (?, ?, ?)
            """,
            (name, description, category)
        )
        conn.commit()
        return cursor.lastrowid


class MembershipRepository:
    """Repository handling Club Membership associations."""

    def __init__(self, db=None):
        self.db = db

    def _get_conn(self):
        return self.db if self.db is not None else get_db()

    def get_user_memberships(self, user_id):
        cursor = self._get_conn().cursor()
        cursor.execute(
            """
            SELECT m.*, c.name as club_name, c.category as club_category
            FROM memberships m
            JOIN clubs c ON m.club_id = c.id
            WHERE m.user_id = ?
            """,
            (user_id,)
        )
        return cursor.fetchall()

    def get_club_members(self, club_id):
        cursor = self._get_conn().cursor()
        cursor.execute(
            """
            SELECT m.*, u.username, u.full_name, u.email
            FROM memberships m
            JOIN users u ON m.user_id = u.id
            WHERE m.club_id = ?
            """,
            (club_id,)
        )
        return cursor.fetchall()

    def add_membership(self, user_id, club_id):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO memberships (user_id, club_id, status)
            VALUES (?, ?, 'ACTIVE')
            """,
            (user_id, club_id)
        )
        conn.commit()
        return cursor.lastrowid

    def exists(self, user_id, club_id):
        cursor = self._get_conn().cursor()
        cursor.execute(
            "SELECT id FROM memberships WHERE user_id = ? AND club_id = ?",
            (user_id, club_id)
        )
        return cursor.fetchone() is not None


class EventRepository:
    """Repository handling Event entity operations."""

    def __init__(self, db=None):
        self.db = db

    def _get_conn(self):
        return self.db if self.db is not None else get_db()

    def count(self):
        """Return total count of scheduled events (CS05 centralization)."""
        cursor = self._get_conn().cursor()
        cursor.execute("SELECT COUNT(*) AS total FROM events")
        row = cursor.fetchone()
        return row["total"] if row else 0

    def get_all(self):
        cursor = self._get_conn().cursor()
        cursor.execute(
            """
            SELECT e.*, c.name as club_name, u.full_name as organizer_name
            FROM events e
            JOIN clubs c ON e.club_id = c.id
            JOIN users u ON e.created_by = u.id
            ORDER BY e.event_date ASC
            """
        )
        return cursor.fetchall()

    def get_by_id(self, event_id):
        cursor = self._get_conn().cursor()
        cursor.execute(
            """
            SELECT e.*, c.name as club_name
            FROM events e
            JOIN clubs c ON e.club_id = c.id
            WHERE e.id = ?
            """,
            (event_id,)
        )
        return cursor.fetchone()

    def get_by_club(self, club_id):
        cursor = self._get_conn().cursor()
        cursor.execute(
            """
            SELECT * FROM events
            WHERE club_id = ?
            ORDER BY event_date ASC
            """,
            (club_id,)
        )
        return cursor.fetchall()

    def create(self, club_id, title, description, event_date, location,
               created_by):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO events (
                club_id, title, description, event_date, location, created_by
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (club_id, title, description, event_date, location, created_by)
        )
        conn.commit()
        return cursor.lastrowid

    def update(self, event_id, title, description, event_date, location):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE events
            SET title = ?, description = ?, event_date = ?, location = ?
            WHERE id = ?
            """,
            (title, description, event_date, location, event_id)
        )
        conn.commit()


class RegistrationRepository:
    """Repository handling Event Registration records."""

    def __init__(self, db=None):
        self.db = db

    def _get_conn(self):
        return self.db if self.db is not None else get_db()

    def register(self, event_id, user_id):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO event_registrations (event_id, user_id, status)
            VALUES (?, ?, 'REGISTERED')
            """,
            (event_id, user_id)
        )
        conn.commit()
        return cursor.lastrowid

    def exists(self, event_id, user_id):
        cursor = self._get_conn().cursor()
        cursor.execute(
            """
            SELECT id FROM event_registrations
            WHERE event_id = ? AND user_id = ?
            """,
            (event_id, user_id)
        )
        return cursor.fetchone() is not None

    def get_user_registrations(self, user_id):
        cursor = self._get_conn().cursor()
        cursor.execute(
            """
            SELECT r.*, e.title as event_title, e.event_date,
                   e.location, c.name as club_name
            FROM event_registrations r
            JOIN events e ON r.event_id = e.id
            JOIN clubs c ON e.club_id = c.id
            WHERE r.user_id = ?
            """,
            (user_id,)
        )
        return cursor.fetchall()


class AnnouncementRepository:
    """Repository handling Announcement publishing and queries."""

    def __init__(self, db=None):
        self.db = db

    def _get_conn(self):
        return self.db if self.db is not None else get_db()

    def get_all(self):
        cursor = self._get_conn().cursor()
        cursor.execute(
            """
            SELECT a.*, c.name as club_name, u.full_name as author_name
            FROM announcements a
            JOIN clubs c ON a.club_id = c.id
            JOIN users u ON a.created_by = u.id
            ORDER BY a.created_at DESC
            """
        )
        return cursor.fetchall()

    def create(self, club_id, title, content, created_by):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO announcements (club_id, title, content, created_by)
            VALUES (?, ?, ?, ?)
            """,
            (club_id, title, content, created_by)
        )
        conn.commit()
        return cursor.lastrowid


class AuditRepository:
    """Repository managing audit trail logging."""

    def __init__(self, db=None):
        self.db = db

    def _get_conn(self):
        return self.db if self.db is not None else get_db()

    def log(self, user_id, action, details):
        conn = self._get_conn()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO audit_logs (user_id, action, details)
            VALUES (?, ?, ?)
            """,
            (user_id, action, details)
        )
        conn.commit()
        return cursor.lastrowid

    def get_all(self):
        cursor = self._get_conn().cursor()
        cursor.execute(
            """
            SELECT a.*, u.username
            FROM audit_logs a
            LEFT JOIN users u ON a.user_id = u.id
            ORDER BY a.timestamp DESC
            """
        )
        return cursor.fetchall()
