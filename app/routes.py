"""
Routes and Presentation Controllers for College Club Management System (v0.1)
"""

import sqlite3
from flask import (
    Blueprint, render_template, request, redirect, url_for, session, flash, current_app
)
from .services import (
    AuthenticationService,
    ClubService,
    MembershipService,
    EventService,
    RegistrationService,
    AnnouncementService,
    AuditService
)
from .repositories import UserRepository

bp = Blueprint('routes', __name__)

auth_service = AuthenticationService()
club_service = ClubService()
membership_service = MembershipService()
event_service = EventService()
registration_service = RegistrationService()
announcement_service = AnnouncementService()
audit_service = AuditService()
user_repo = UserRepository()


# CS05: Duplicated direct database access logic in route helper
def get_quick_stats():
    """Quick helper that opens its own connection instead of using repository layer."""
    conn = sqlite3.connect(current_app.config['DATABASE'])
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM clubs")
    total_clubs = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM events")
    total_events = cur.fetchone()[0]
    conn.close()
    return total_clubs, total_events


@bp.route('/')
def index():
    if 'user_id' in session:
        role = session.get('role')
        # CS03: Role dispatch chain
        if role == 'student':
            return redirect(url_for('routes.student_dashboard'))
        elif role == 'coordinator':
            return redirect(url_for('routes.coordinator_dashboard'))
        elif role == 'admin':
            return redirect(url_for('routes.admin_dashboard'))
    return redirect(url_for('routes.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user, err = auth_service.authenticate(username, password)
        if err:
            flash(err, 'danger')
            return render_template('login.html')

        # Set session variables
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = user['role']
        session['full_name'] = user['full_name']
        session['club_id'] = user['club_id']

        flash(f"Welcome back, {user['full_name']}!", 'success')

        # CS03 & CS04: Role dispatching with hardcoded strings
        if user['role'] == 'student':
            return redirect(url_for('routes.student_dashboard'))
        elif user['role'] == 'coordinator':
            return redirect(url_for('routes.coordinator_dashboard'))
        elif user['role'] == 'admin':
            return redirect(url_for('routes.admin_dashboard'))
        else:
            return redirect(url_for('routes.login'))

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('routes.login'))


# ============================================================
# STUDENT ROUTES
# ============================================================

@bp.route('/student')
def student_dashboard():
    # CS01: Duplicated authorization check
    if 'user_id' not in session or session.get('role') != 'student':
        flash("Unauthorized: Student access only.", "danger")
        return redirect(url_for('routes.login'))

    user_id = session.get('user_id')
    clubs = club_service.get_all_clubs()
    my_memberships = membership_service.get_user_memberships(user_id)
    my_club_ids = [m['club_id'] for m in my_memberships]

    events = event_service.get_all_events()
    my_registrations = registration_service.get_user_registrations(user_id)
    my_reg_event_ids = [r['event_id'] for r in my_registrations]

    announcements = announcement_service.get_all_announcements()

    return render_template(
        'student.html',
        clubs=clubs,
        my_club_ids=my_club_ids,
        events=events,
        my_reg_event_ids=my_reg_event_ids,
        announcements=announcements
    )


@bp.route('/student/clubs/join', methods=['POST'])
def student_join_club():
    # CS01: Duplicated authorization check
    if 'user_id' not in session or session.get('role') != 'student':
        flash("Unauthorized: Student access only.", "danger")
        return redirect(url_for('routes.login'))

    user_id = session.get('user_id')
    club_id = request.form.get('club_id')

    success, msg = membership_service.join_club(user_id, club_id)
    if success:
        flash("Successfully joined the club!", "success")
    else:
        # SEC04: Raw error message exposure
        flash(msg, "warning")

    return redirect(url_for('routes.student_dashboard'))


@bp.route('/student/events/register', methods=['POST'])
def student_register_event():
    # CS01: Duplicated authorization check
    if 'user_id' not in session or session.get('role') != 'student':
        flash("Unauthorized: Student access only.", "danger")
        return redirect(url_for('routes.login'))

    user_id = session.get('user_id')
    event_id = request.form.get('event_id')

    success, msg = registration_service.register_for_event(event_id, user_id)
    if success:
        flash("Successfully registered for the event!", "success")
    else:
        flash(msg, "warning")

    return redirect(url_for('routes.student_dashboard'))


# ============================================================
# COORDINATOR ROUTES
# ============================================================

@bp.route('/coordinator')
def coordinator_dashboard():
    # CS01: Duplicated authorization check
    if 'user_id' not in session or session.get('role') != 'coordinator':
        flash("Unauthorized: Coordinator access only.", "danger")
        return redirect(url_for('routes.login'))

    club_id = session.get('club_id')
    club = club_service.get_club_by_id(club_id) if club_id else None

    club_events = event_service.get_club_events(club_id) if club_id else []
    all_events = event_service.get_all_events()
    members = membership_service.get_club_members(club_id) if club_id else []
    announcements = announcement_service.get_all_announcements()

    return render_template(
        'coordinator.html',
        club=club,
        club_events=club_events,
        all_events=all_events,
        members=members,
        announcements=announcements
    )


@bp.route('/coordinator/events/create', methods=['POST'])
def coordinator_create_event():
    # CS01: Duplicated authorization check
    if 'user_id' not in session or session.get('role') != 'coordinator':
        flash("Unauthorized: Coordinator access only.", "danger")
        return redirect(url_for('routes.login'))

    club_id = session.get('club_id')
    user_id = session.get('user_id')
    title = request.form.get('title')
    description = request.form.get('description')
    event_date = request.form.get('event_date')
    location = request.form.get('location')

    success, res = event_service.create_event_with_notifications_and_audit(
        club_id, title, description, event_date, location, user_id
    )

    if success:
        flash("Event and announcement published successfully!", "success")
    else:
        # SEC04: Raw message exposure
        flash(f"Failed to create event: {res}", "danger")

    return redirect(url_for('routes.coordinator_dashboard'))


@bp.route('/coordinator/events/edit', methods=['POST'])
def coordinator_edit_event():
    """
    SEC02 VULNERABILITY:
    In v0.1, the coordinator passes event_id and edits it.
    The system does NOT verify if the event actually belongs to this coordinator's assigned club!
    """
    # CS01: Duplicated authorization check
    if 'user_id' not in session or session.get('role') not in ['coordinator', 'admin']:
        flash("Unauthorized: Only coordinators can edit events.", "danger")
        return redirect(url_for('routes.login'))

    event_id = request.form.get('event_id')
    title = request.form.get('title')
    description = request.form.get('description')
    event_date = request.form.get('event_date')
    location = request.form.get('location')

    success, msg = event_service.update_event(
        event_id=event_id,
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        user_role=session.get('role'),
        user_club_id=session.get('club_id')
    )

    if success:
        flash("Event modified successfully!", "success")
    else:
        flash(msg, "danger")

    return redirect(url_for('routes.coordinator_dashboard'))


@bp.route('/coordinator/announcements/create', methods=['POST'])
def coordinator_create_announcement():
    # CS01: Duplicated authorization check
    if 'user_id' not in session or session.get('role') != 'coordinator':
        flash("Unauthorized: Coordinator access only.", "danger")
        return redirect(url_for('routes.login'))

    club_id = session.get('club_id')
    user_id = session.get('user_id')
    title = request.form.get('title')
    content = request.form.get('content')

    success, res = announcement_service.publish_announcement(
        club_id, title, content, user_id, session.get('role')
    )

    if success:
        flash("Announcement published successfully!", "success")
    else:
        flash(f"Announcement failed: {res}", "danger")

    return redirect(url_for('routes.coordinator_dashboard'))


# ============================================================
# ADMINISTRATOR ROUTES
# ============================================================

@bp.route('/admin')
def admin_dashboard():
    # CS01: Duplicated authorization check
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Unauthorized: Administrator access only.", "danger")
        return redirect(url_for('routes.login'))

    clubs = club_service.get_all_clubs()
    coordinators = user_repo.get_coordinators()
    audit_logs = audit_service.get_audit_trail(session.get('role'))
    total_clubs, total_events = get_quick_stats()

    return render_template(
        'admin.html',
        clubs=clubs,
        coordinators=coordinators,
        audit_logs=audit_logs,
        total_clubs=total_clubs,
        total_events=total_events
    )


@bp.route('/admin/clubs/create', methods=['POST'])
def admin_create_club():
    # CS01: Duplicated authorization check
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Unauthorized: Administrator access only.", "danger")
        return redirect(url_for('routes.login'))

    name = request.form.get('name')
    description = request.form.get('description')
    category = request.form.get('category')

    success, res = club_service.create_club(name, description, category, session.get('user_id'))
    if success:
        flash(f"Club '{name}' created successfully!", "success")
    else:
        flash(f"Error creating club: {res}", "danger")

    return redirect(url_for('routes.admin_dashboard'))


@bp.route('/admin/coordinators/assign', methods=['POST'])
def admin_assign_coordinator():
    # CS01: Duplicated authorization check
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Unauthorized: Administrator access only.", "danger")
        return redirect(url_for('routes.login'))

    user_id = request.form.get('user_id')
    club_id = request.form.get('club_id')

    try:
        user_repo.update_coordinator_club(user_id, club_id)
        # Note: missing audit log for coordinator assignment in v0.1 (SEC05)
        flash("Coordinator assigned to club successfully!", "success")
    except Exception as e:
        # SEC04: Exposing raw error
        flash(f"Assignment error: {str(e)}", "danger")

    return redirect(url_for('routes.admin_dashboard'))
