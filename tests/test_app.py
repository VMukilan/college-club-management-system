"""
Unit and Functional Tests for College Club Management System (v0.3 Secure)

Tests encompass functional user flows and Critical Security Scenarios:
1. Student login
2. Coordinator login
3. Administrator login
4. View clubs
5. Join club
6. View events
7. Event registration
8. Event creation
9. Announcement creation
10. Invalid login rejection
11. Unauthenticated access redirection
12. Critical Security Scenario: Coordinator modifies OWN club event -> ALLOW
13. Critical Security Scenario: Coordinator modifies OTHER club event -> DENY
14. Critical Security Scenario: Student attempts event modification -> DENY
15. Critical Security Scenario: Admin modifies event -> ALLOW
16. Security Auditing: Failed login recorded in AUDIT_LOG
17. Security Auditing: Unauthorized event edit recorded as AUTHZ_FAILURE
18. Input Validation: Malformed / oversized event title rejected
"""


def test_student_login(client):
    """Test successful student login and redirect to student portal."""
    response = client.post("/login", data={
        "username": "student_alice",
        "password": "StudentPass123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Student Portal" in response.data
    assert b"Alice Smith" in response.data


def test_coordinator_login(client):
    """Test successful coordinator login and redirect to coordinator portal."""
    response = client.post("/login", data={
        "username": "coord_robotics",
        "password": "CoordPass123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Club Coordinator Portal" in response.data
    assert b"Robotics Club" in response.data


def test_admin_login(client):
    """Test successful admin login and redirect to admin control center."""
    response = client.post("/login", data={
        "username": "admin",
        "password": "AdminPass123"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Administrator Control Center" in response.data
    assert b"System Administrator" in response.data


def test_view_clubs(client):
    """Test that a logged-in student can view available clubs."""
    client.post("/login", data={
        "username": "student_alice",
        "password": "StudentPass123"
    })
    response = client.get("/student")
    assert response.status_code == 200
    assert b"Robotics Club" in response.data
    assert b"Coding Club" in response.data
    assert b"Literary Club" in response.data


def test_join_club(client):
    """Test student joining a club."""
    client.post("/login", data={
        "username": "student_bob",
        "password": "StudentPass123"
    })
    response = client.post("/student/clubs/join", data={
        "club_id": 2
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Successfully joined the club!" in response.data


def test_view_events(client):
    """Test viewing scheduled events on student dashboard."""
    client.post("/login", data={
        "username": "student_alice",
        "password": "StudentPass123"
    })
    response = client.get("/student")
    assert response.status_code == 200
    assert b"RoboWars 2026" in response.data
    assert b"Hackathon 2026" in response.data


def test_event_registration(client):
    """Test student registering for an upcoming event."""
    client.post("/login", data={
        "username": "student_alice",
        "password": "StudentPass123"
    })
    response = client.post("/student/events/register", data={
        "event_id": 1
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Successfully registered for the event!" in response.data


def test_event_creation(client):
    """Test coordinator creating a new event."""
    client.post("/login", data={
        "username": "coord_robotics",
        "password": "CoordPass123"
    })
    response = client.post("/coordinator/events/create", data={
        "title": "Autonomous Drone Workshop",
        "event_date": "2026-12-05",
        "location": "Lab 101",
        "description": "Hands-on tutorial building micro drones."
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Event and announcement published successfully!" in response.data
    assert b"Autonomous Drone Workshop" in response.data


def test_announcement_creation(client):
    """Test coordinator creating and publishing an announcement."""
    client.post("/login", data={
        "username": "coord_robotics",
        "password": "CoordPass123"
    })
    response = client.post("/coordinator/announcements/create", data={
        "title": "Mid-semester General Body Meeting",
        "content": "All club members must attend meeting in Seminar Hall."
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Announcement published successfully!" in response.data


def test_invalid_login(client):
    """Test login with wrong password."""
    response = client.post("/login", data={
        "username": "admin",
        "password": "WrongPassword999"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data


def test_unauthenticated_access_redirect(client):
    """Test that unauthorized access to protected dashboard redirects."""
    response = client.get("/student", follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign In" in response.data


# ============================================================
# CRITICAL SECURITY SCENARIO TESTS (Section 23 Master Prompt)
# ============================================================

def test_sec02_own_club_event_modification_allowed(client):
    """
    CRITICAL SECURITY SCENARIO 1:
    Coordinator belonging to Club A modifies Club A event -> ALLOW
    coord_robotics (Club 1) modifies Event 1 (Club 1 RoboWars).
    """
    client.post("/login", data={
        "username": "coord_robotics",
        "password": "CoordPass123"
    })
    response = client.post("/coordinator/events/edit", data={
        "event_id": 1,
        "title": "RoboWars 2026 - Official Reschedule",
        "event_date": "2026-11-18",
        "location": "Arena Floor A",
        "description": "Updated schedule for robotics club members."
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Event modified successfully!" in response.data


def test_sec02_cross_club_event_modification_denied(client):
    """
    CRITICAL SECURITY SCENARIO 2 (SEC02 Enforcement):
    Coordinator belonging to Club A modifies Club B event -> DENY
    coord_robotics (Club 1) attempts to modify Event 2 (belongs to Club 2).
    In v0.3, this MUST BE DENIED!
    """
    client.post("/login", data={
        "username": "coord_robotics",
        "password": "CoordPass123"
    })
    response = client.post("/coordinator/events/edit", data={
        "event_id": 2,
        "title": "Tampered Hackathon Title",
        "event_date": "2026-11-20",
        "location": "Unauthorized Room",
        "description": "Tampered description across club boundary."
    }, follow_redirects=True)
    assert response.status_code == 200
    assert (
        b"Access Denied: You are not authorized to modify events "
        b"for another club."
    ) in response.data


def test_student_event_modification_denied(client):
    """
    CRITICAL SECURITY SCENARIO 3:
    Student attempts to modify event -> DENY
    """
    client.post("/login", data={
        "username": "student_alice",
        "password": "StudentPass123"
    })
    response = client.post("/coordinator/events/edit", data={
        "event_id": 1,
        "title": "Student Defaced Event",
        "event_date": "2026-11-20",
        "location": "Anywhere",
        "description": "Student tamper attempt."
    }, follow_redirects=True)
    assert response.status_code == 200
    # Denied by role decorator
    assert (
        b"Unauthorized access" in response.data
        or b"Sign In" in response.data
    )


def test_admin_event_modification_allowed(client):
    """
    CRITICAL SECURITY SCENARIO 4:
    Administrator performs authorized administrative event operation -> ALLOW
    admin modifies Event 2 (Coding Club event) under administrative oversight.
    """
    client.post("/login", data={
        "username": "admin",
        "password": "AdminPass123"
    })
    response = client.post("/coordinator/events/edit", data={
        "event_id": 2,
        "title": "Hackathon 2026 - Admin Verified Schedule",
        "event_date": "2026-11-22",
        "location": "Main Auditorium & Labs",
        "description": "Administrative update to venue and timings."
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Event modified successfully!" in response.data


def test_failed_login_creates_audit_log(app, client):
    """
    SECURITY AUDITING (SEC05):
    Verify that failed login attempts write to the AUDIT_LOG table.
    """
    client.post("/login", data={
        "username": "admin",
        "password": "BadPassword123"
    })
    with app.app_context():
        from app.database import get_db
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM audit_logs WHERE action = 'LOGIN_FAILURE' "
            "ORDER BY id DESC LIMIT 1"
        )
        log = cur.fetchone()
        assert log is not None
        assert "Failed password verification" in log["details"]


def test_cross_club_tamper_creates_audit_log(app, client):
    """
    SECURITY AUDITING (SEC05):
    Verify that unauthorized cross-club edit attempts create an AUTHZ_FAILURE
    audit log entry.
    """
    client.post("/login", data={
        "username": "coord_robotics",
        "password": "CoordPass123"
    })
    client.post("/coordinator/events/edit", data={
        "event_id": 2,
        "title": "Blocked Tamper",
        "event_date": "2026-11-20",
        "location": "Room X",
        "description": "Should fail and generate audit."
    })
    with app.app_context():
        from app.database import get_db
        db = get_db()
        cur = db.cursor()
        cur.execute(
            "SELECT * FROM audit_logs WHERE action = 'AUTHZ_FAILURE' "
            "ORDER BY id DESC LIMIT 1"
        )
        log = cur.fetchone()
        assert log is not None
        assert "Cross-club modification DENIED" in log["details"]


def test_input_validation_bounds(client):
    """
    INPUT SECURITY (SEC03):
    Verify that malformed / short event titles are rejected by validation.
    """
    client.post("/login", data={
        "username": "coord_robotics",
        "password": "CoordPass123"
    })
    response = client.post("/coordinator/events/create", data={
        "title": "AB",  # Under minimum 3 characters
        "event_date": "2026-12-01",
        "location": "Lab",
        "description": "Short title test."
    }, follow_redirects=True)
    assert response.status_code == 200
    assert (
        b"Event title must be at least 3 character(s) long." in response.data
    )
