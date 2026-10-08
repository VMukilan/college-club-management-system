"""
Routes and Presentation Controllers for College Club Management System (v0.2)

Refactoring Highlights (v0.2):
- CS01: Replaced duplicated authorization checks with @login_required and
        @roles_accepted decorators.
- CS04: Replaced hardcoded role strings with Role constants.
- CS05: Removed direct sqlite3 connection in get_quick_stats(); now uses
        Repository count() methods.
- CS06: Improved error feedback without raw implementation leakage.
"""

import logging
from flask import (
    Blueprint, render_template, request, redirect, url_for, session, flash
)
from .constants import Role
from .auth_decorators import roles_accepted
from .services import (
    AuthenticationService,
    ClubService,
    MembershipService,
    EventService,
    RegistrationService,
    AnnouncementService,
    AuditService
)
from .repositories import UserRepository, ClubRepository, EventRepository

logger = logging.getLogger(__name__)

bp = Blueprint("routes", __name__)

auth_service = AuthenticationService()
club_service = ClubService()
membership_service = MembershipService()
event_service = EventService()
registration_service = RegistrationService()
announcement_service = AnnouncementService()
audit_service = AuditService()
user_repo = UserRepository()
club_repo = ClubRepository()
event_repo = EventRepository()


@bp.route("/")
def index():
    if "user_id" in session:
        role = session.get("role")
        if role == Role.STUDENT:
            return redirect(url_for("routes.student_dashboard"))
        elif role == Role.COORDINATOR:
            return redirect(url_for("routes.coordinator_dashboard"))
        elif role == Role.ADMIN:
            return redirect(url_for("routes.admin_dashboard"))
    return redirect(url_for("routes.login"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user, err = auth_service.authenticate(username, password)
        if err:
            flash(err, "danger")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        session["full_name"] = user["full_name"]
        session["club_id"] = user["club_id"]

        flash(f"Welcome back, {user['full_name']}!", "success")

        if user["role"] == Role.STUDENT:
            return redirect(url_for("routes.student_dashboard"))
        elif user["role"] == Role.COORDINATOR:
            return redirect(url_for("routes.coordinator_dashboard"))
        elif user["role"] == Role.ADMIN:
            return redirect(url_for("routes.admin_dashboard"))
        else:
            return redirect(url_for("routes.login"))

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for("routes.login"))


# ============================================================
# STUDENT ROUTES (Refactored with CS01 centralized decorators)
# ============================================================

@bp.route("/student")
@roles_accepted(Role.STUDENT)
def student_dashboard():
    user_id = session.get("user_id")
    clubs = club_service.get_all_clubs()
    my_memberships = membership_service.get_user_memberships(user_id)
    my_club_ids = [m["club_id"] for m in my_memberships]

    events = event_service.get_all_events()
    my_registrations = registration_service.get_user_registrations(user_id)
    my_reg_event_ids = [r["event_id"] for r in my_registrations]

    announcements = announcement_service.get_all_announcements()

    return render_template(
        "student.html",
        clubs=clubs,
        my_club_ids=my_club_ids,
        events=events,
        my_reg_event_ids=my_reg_event_ids,
        announcements=announcements
    )


@bp.route("/student/clubs/join", methods=["POST"])
@roles_accepted(Role.STUDENT)
def student_join_club():
    user_id = session.get("user_id")
    club_id = request.form.get("club_id")

    success, msg = membership_service.join_club(user_id, club_id)
    if success:
        flash("Successfully joined the club!", "success")
    else:
        flash(msg, "warning")

    return redirect(url_for("routes.student_dashboard"))


@bp.route("/student/events/register", methods=["POST"])
@roles_accepted(Role.STUDENT)
def student_register_event():
    user_id = session.get("user_id")
    event_id = request.form.get("event_id")

    success, msg = registration_service.register_for_event(event_id, user_id)
    if success:
        flash("Successfully registered for the event!", "success")
    else:
        flash(msg, "warning")

    return redirect(url_for("routes.student_dashboard"))


# ============================================================
# COORDINATOR ROUTES (Refactored with CS01 centralized decorators)
# ============================================================

@bp.route("/coordinator")
@roles_accepted(Role.COORDINATOR)
def coordinator_dashboard():
    club_id = session.get("club_id")
    club = club_service.get_club_by_id(club_id) if club_id else None

    club_events = event_service.get_club_events(club_id) if club_id else []
    all_events = event_service.get_all_events()
    members = membership_service.get_club_members(club_id) if club_id else []
    announcements = announcement_service.get_all_announcements()

    return render_template(
        "coordinator.html",
        club=club,
        club_events=club_events,
        all_events=all_events,
        members=members,
        announcements=announcements
    )


@bp.route("/coordinator/events/create", methods=["POST"])
@roles_accepted(Role.COORDINATOR)
def coordinator_create_event():
    club_id = session.get("club_id")
    user_id = session.get("user_id")
    title = request.form.get("title")
    description = request.form.get("description")
    event_date = request.form.get("event_date")
    location = request.form.get("location")

    success, res = event_service.create_event_with_notifications_and_audit(
        club_id, title, description, event_date, location, user_id
    )

    if success:
        flash("Event and announcement published successfully!", "success")
    else:
        flash(f"Failed to create event: {res}", "danger")

    return redirect(url_for("routes.coordinator_dashboard"))


@bp.route("/coordinator/events/edit", methods=["POST"])
@roles_accepted(Role.COORDINATOR, Role.ADMIN)
def coordinator_edit_event():
    event_id = request.form.get("event_id")
    title = request.form.get("title")
    description = request.form.get("description")
    event_date = request.form.get("event_date")
    location = request.form.get("location")

    success, msg = event_service.update_event(
        event_id=event_id,
        title=title,
        description=description,
        event_date=event_date,
        location=location,
        user_role=session.get("role"),
        user_club_id=session.get("club_id")
    )

    if success:
        flash("Event modified successfully!", "success")
    else:
        flash(msg, "danger")

    return redirect(url_for("routes.coordinator_dashboard"))


@bp.route("/coordinator/announcements/create", methods=["POST"])
@roles_accepted(Role.COORDINATOR)
def coordinator_create_announcement():
    club_id = session.get("club_id")
    user_id = session.get("user_id")
    title = request.form.get("title")
    content = request.form.get("content")

    success, res = announcement_service.publish_announcement(
        club_id, title, content, user_id, session.get("role")
    )

    if success:
        flash("Announcement published successfully!", "success")
    else:
        flash(f"Announcement failed: {res}", "danger")

    return redirect(url_for("routes.coordinator_dashboard"))


# ============================================================
# ADMINISTRATOR ROUTES (Refactored with CS01 centralized decorators)
# ============================================================

@bp.route("/admin")
@roles_accepted(Role.ADMIN)
def admin_dashboard():
    clubs = club_service.get_all_clubs()
    coordinators = user_repo.get_coordinators()
    audit_logs = audit_service.get_audit_trail(session.get("role"))

    # CS05 Refactoring: Use repository count() instead of raw sql connection
    total_clubs = club_repo.count()
    total_events = event_repo.count()

    return render_template(
        "admin.html",
        clubs=clubs,
        coordinators=coordinators,
        audit_logs=audit_logs,
        total_clubs=total_clubs,
        total_events=total_events
    )


@bp.route("/admin/clubs/create", methods=["POST"])
@roles_accepted(Role.ADMIN)
def admin_create_club():
    name = request.form.get("name")
    description = request.form.get("description")
    category = request.form.get("category")

    success, res = club_service.create_club(
        name, description, category, session.get("user_id")
    )
    if success:
        flash(f"Club '{name}' created successfully!", "success")
    else:
        flash(f"Error creating club: {res}", "danger")

    return redirect(url_for("routes.admin_dashboard"))


@bp.route("/admin/coordinators/assign", methods=["POST"])
@roles_accepted(Role.ADMIN)
def admin_assign_coordinator():
    user_id = request.form.get("user_id")
    club_id = request.form.get("club_id")

    try:
        user_repo.update_coordinator_club(user_id, club_id)
        flash("Coordinator assigned to club successfully!", "success")
    except Exception as err:
        logger.error("Error assigning coordinator: %s", err)
        flash("Failed to update coordinator assignment.", "danger")

    return redirect(url_for("routes.admin_dashboard"))
