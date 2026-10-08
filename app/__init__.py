"""
Application Factory for College Club Management System (v0.2 Refactored)
Addresses CS04: Loads configuration dynamically from structured Config class.
"""

import os
from flask import Flask
from .config import Config
from .database import init_db


def create_app(test_config=None):
    """Factory function initializing Flask app, database, and blueprints."""
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    # CS04 Refactoring: Configuration loaded from Config class / environment
    app.config.from_object(Config)

    # Set default database path in instance folder if not customized
    if "DATABASE" not in app.config:
        app.config["DATABASE"] = os.path.join(
            app.instance_path,
            app.config.get("DATABASE_NAME", "college_club.db")
        )

    if test_config is not None:
        app.config.update(test_config)

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Initialize database schema and default seeds
    init_db(app)

    # Register blueprints
    from . import routes
    app.register_blueprint(routes.bp)

    return app
