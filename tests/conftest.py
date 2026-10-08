import os
import tempfile
import pytest
from app import create_app
from app.database import init_db

@pytest.fixture
def app():
    # Create temporary database file for isolation
    db_fd, db_path = tempfile.mkstemp()

    test_app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
        'SECRET_KEY': 'test_secret_key_v0.1'
    })

    yield test_app

    os.close(db_fd)
    try:
        os.unlink(db_path)
    except OSError:
        pass

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
