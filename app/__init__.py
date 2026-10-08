import os
from flask import Flask
from .database import init_db

def create_app(test_config=None):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # CS04: Hard-coded configuration values
    app.config.from_mapping(
        SECRET_KEY="dev_hardcoded_secret_key_v0.1_dont_use_in_prod",
        DATABASE=os.path.join(app.instance_path, "college_club.db"),
    )

    if test_config is not None:
        app.config.update(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Initialize the database schema and default seed data
    init_db(app)

    # Register routes
    from . import routes
    app.register_blueprint(routes.bp)

    return app
