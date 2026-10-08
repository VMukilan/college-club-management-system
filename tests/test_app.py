"""
Unit and Functional Tests for College Club Management System (v0.1)

Required test cases:
1. Student login
2. Coordinator login
3. Administrator login
4. View clubs
5. Join club
6. View events
7. Event registration
8. Event creation
9. Announcement creation
"""

import pytest

def test_student_login(client):
    """Test successful student login and redirect to student portal."""
    response = client.post('/login', data={
        'username': 'student_alice',
        'password': 'StudentPass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Student Portal" in response.data
    assert b"Alice Smith" in response.data

def test_coordinator_login(client):
    """Test successful coordinator login and redirect to coordinator portal."""
    response = client.post('/login', data={
        'username': 'coord_robotics',
        'password': 'CoordPass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Club Coordinator Portal" in response.data
    assert b"Robotics Club" in response.data

def test_admin_login(client):
    """Test successful administrator login and redirect to admin control center."""
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'AdminPass123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Administrator Control Center" in response.data
    assert b"System Administrator" in response.data

def test_view_clubs(client):
    """Test that a logged-in student can view available clubs."""
    # Log in as student
    client.post('/login', data={
        'username': 'student_alice',
        'password': 'StudentPass123'
    })
    response = client.get('/student')
    assert response.status_code == 200
    assert b"Robotics Club" in response.data
    assert b"Coding Club" in response.data
    assert b"Literary Club" in response.data

def test_join_club(client):
    """Test student joining a club."""
    # Log in as student_bob
    client.post('/login', data={
        'username': 'student_bob',
        'password': 'StudentPass123'
    })
    # Join Coding Club (ID: 2)
    response = client.post('/student/clubs/join', data={
        'club_id': 2
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Successfully joined the club!" in response.data

def test_view_events(client):
    """Test viewing scheduled events on student dashboard."""
    client.post('/login', data={
        'username': 'student_alice',
        'password': 'StudentPass123'
    })
    response = client.get('/student')
    assert response.status_code == 200
    assert b"RoboWars 2026" in response.data
    assert b"Hackathon 2026" in response.data

def test_event_registration(client):
    """Test student registering for an upcoming event."""
    client.post('/login', data={
        'username': 'student_alice',
        'password': 'StudentPass123'
    })
    response = client.post('/student/events/register', data={
        'event_id': 1
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Successfully registered for the event!" in response.data

def test_event_creation(client):
    """Test coordinator creating a new event."""
    # Log in as coordinator
    client.post('/login', data={
        'username': 'coord_robotics',
        'password': 'CoordPass123'
    })
    response = client.post('/coordinator/events/create', data={
        'title': 'Autonomous Drone Workshop',
        'event_date': '2026-12-05',
        'location': 'Lab 101',
        'description': 'Hands-on tutorial building micro drones.'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Event and announcement published successfully!" in response.data
    assert b"Autonomous Drone Workshop" in response.data

def test_announcement_creation(client):
    """Test coordinator creating and publishing an announcement."""
    client.post('/login', data={
        'username': 'coord_robotics',
        'password': 'CoordPass123'
    })
    response = client.post('/coordinator/announcements/create', data={
        'title': 'Mid-semester General Body Meeting',
        'content': 'All club members must attend the meeting at 4 PM in Seminar Hall.'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Announcement published successfully!" in response.data

def test_invalid_login(client):
    """Test login with wrong password."""
    response = client.post('/login', data={
        'username': 'admin',
        'password': 'WrongPassword999'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

def test_unauthenticated_access_redirect(client):
    """Test that unauthorized access to protected dashboard redirects to login."""
    response = client.get('/student', follow_redirects=True)
    assert response.status_code == 200
    assert b"Sign In" in response.data

def test_sec02_unauthorized_cross_club_event_modification_v0_1(client):
    """
    SEC02 Verification in v0.1:
    Demonstrates controlled vulnerability SEC02.
    Coordinator of Club 1 (coord_robotics) modifies Event 2 (Hackathon 2026 belonging to Coding Club).
    In v0.1, this succeeds because club-level authorization is missing!
    """
    # Login as coord_robotics (Club 1)
    client.post('/login', data={
        'username': 'coord_robotics',
        'password': 'CoordPass123'
    })
    # Tamper with Event 2 (belongs to Coding Club ID: 2)
    response = client.post('/coordinator/events/edit', data={
        'event_id': 2,
        'title': 'Hackathon 2026 - Tampered by Other Coordinator',
        'event_date': '2026-11-20',
        'location': 'Unauthorized Location',
        'description': 'Tampered description from another club coordinator.'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Event modified successfully!" in response.data

