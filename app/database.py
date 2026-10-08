"""
Database management for College Club Management System (v0.3 Secure Release)
Database Engine: SQLite
"""

import sqlite3
from flask import current_app, g
from werkzeug.security import generate_password_hash


def get_db():
    """Get database connection for current Flask request context."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close database connection at end of request."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    """Initialize database tables and seed initial sample data."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # USER table with is_active status validation
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                club_id INTEGER,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (club_id) REFERENCES clubs (id)
            )
        """)

        # Migration helper for existing databases
        try:
            cursor.execute(
                "ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1"
            )
        except sqlite3.OperationalError:
            pass

        # CLUB table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clubs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # MEMBERSHIP table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memberships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                club_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'ACTIVE',
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, club_id),
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (club_id) REFERENCES clubs (id)
            )
        """)

        # EVENT table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                club_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                event_date TEXT NOT NULL,
                location TEXT NOT NULL,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (club_id) REFERENCES clubs (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        """)

        # EVENT_REGISTRATION table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'REGISTERED',
                registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(event_id, user_id),
                FOREIGN KEY (event_id) REFERENCES events (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        # ANNOUNCEMENT table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS announcements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                club_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_by INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (club_id) REFERENCES clubs (id),
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        """)

        # AUDIT_LOG table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                details TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)

        db.commit()
        seed_initial_data(db)


def seed_initial_data(db):
    """Seed initial clubs and users if not already present."""
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM users")
    count = cursor.fetchone()["count"]
    if count == 0:
        cursor.execute(
            """
            INSERT INTO clubs (id, name, description, category)
            VALUES (?, ?, ?, ?)
            """,
            (
                1,
                "Robotics Club",
                "Designing autonomous robots and embedded systems.",
                "Technical"
            )
        )
        cursor.execute(
            """
            INSERT INTO clubs (id, name, description, category)
            VALUES (?, ?, ?, ?)
            """,
            (
                2,
                "Coding Club",
                "Competitive programming and full-stack software development.",
                "Technical"
            )
        )
        cursor.execute(
            """
            INSERT INTO clubs (id, name, description, category)
            VALUES (?, ?, ?, ?)
            """,
            (
                3,
                "Literary Club",
                "Debating, creative writing, elocution, and publications.",
                "Cultural"
            )
        )

        admin_pass = generate_password_hash("AdminPass123")
        coord_pass = generate_password_hash("CoordPass123")
        student_pass = generate_password_hash("StudentPass123")

        cursor.execute(
            """
            INSERT INTO users (
                username, password_hash, role, full_name, email, club_id,
                is_active
            ) VALUES (?, ?, ?, ?, ?, ?, 1)
            """,
            (
                "admin", admin_pass, "admin",
                "System Administrator", "admin@college.edu", None
            )
        )
        cursor.execute(
            """
            INSERT INTO users (
                username, password_hash, role, full_name, email, club_id,
                is_active
            ) VALUES (?, ?, ?, ?, ?, ?, 1)
            """,
            (
                "coord_robotics", coord_pass, "coordinator",
                "Robotics Coordinator", "coord.robotics@college.edu", 1
            )
        )
        cursor.execute(
            """
            INSERT INTO users (
                username, password_hash, role, full_name, email, club_id,
                is_active
            ) VALUES (?, ?, ?, ?, ?, ?, 1)
            """,
            (
                "coord_coding", coord_pass, "coordinator",
                "Coding Club Coordinator", "coord.coding@college.edu", 2
            )
        )
        cursor.execute(
            """
            INSERT INTO users (
                username, password_hash, role, full_name, email, club_id,
                is_active
            ) VALUES (?, ?, ?, ?, ?, ?, 1)
            """,
            (
                "student_alice", student_pass, "student",
                "Alice Smith", "alice@college.edu", None
            )
        )
        cursor.execute(
            """
            INSERT INTO users (
                username, password_hash, role, full_name, email, club_id,
                is_active
            ) VALUES (?, ?, ?, ?, ?, ?, 1)
            """,
            (
                "student_bob", student_pass, "student",
                "Bob Johnson", "bob@college.edu", None
            )
        )

        cursor.execute(
            """
            INSERT INTO events (
                club_id, title, description, event_date, location, created_by
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                "RoboWars 2026",
                "Annual combat robotics tournament for college teams.",
                "2026-11-15",
                "College Indoor Arena",
                2
            )
        )
        cursor.execute(
            """
            INSERT INTO events (
                club_id, title, description, event_date, location, created_by
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                2,
                "Hackathon 2026",
                "24-hour full-stack innovation hackathon.",
                "2026-11-20",
                "Computer Lab 4",
                3
            )
        )

        cursor.execute(
            """
            INSERT INTO announcements (
                club_id, title, content, created_by
            ) VALUES (?, ?, ?, ?)
            """,
            (
                1,
                "RoboWars Registration Open",
                "Registrations are now live for all undergraduates.",
                2
            )
        )
        cursor.execute(
            """
            INSERT INTO announcements (
                club_id, title, content, created_by
            ) VALUES (?, ?, ?, ?)
            """,
            (
                2,
                "Coding Club Weekly Meet",
                "Weekly algorithms discussion every Wednesday 5 PM.",
                3
            )
        )

        cursor.execute(
            """
            INSERT INTO audit_logs (user_id, action, details)
            VALUES (?, ?, ?)
            """,
            (1, "SYSTEM_INIT", "Database initialized with seed data.")
        )

        db.commit()
