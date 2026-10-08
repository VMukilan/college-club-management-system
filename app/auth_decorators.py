"""
Authentication and Authorization Decorators (v0.2 Refactored)
Addresses CS01: Centralizes authentication and role guards,
eliminating code duplication across route handlers.
"""

from functools import wraps
from flask import session, flash, redirect, url_for


def login_required(f):
    """
    Decorator to ensure user is logged in.
    Redirects unauthenticated users to login page.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("routes.login"))
        return f(*args, **kwargs)
    return decorated_function


def roles_accepted(*allowed_roles):
    """
    Decorator to enforce Role-Based Access Control on route handlers.
    Ensures current user possesses at least one of the specified roles.
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("Please sign in to access this page.", "warning")
                return redirect(url_for("routes.login"))

            user_role = session.get("role")
            if user_role not in allowed_roles:
                roles_str = ", ".join(allowed_roles)
                flash(
                    f"Unauthorized access: Requires {roles_str} privileges.",
                    "danger"
                )
                return redirect(url_for("routes.login"))

            return f(*args, **kwargs)
        return decorated_function
    return decorator
