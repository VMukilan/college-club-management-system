"""
Application Configuration Module (v0.2 Refactored)
Addresses CS04: Moves hard-coded configurations into structured config classes.
"""

import os


class Config:
    """
    Base application configuration loaded from environment with fallbacks.
    """
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "dev-refactored-secret-key-v0.2-secure-engineering"
    )
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "college_club.db")
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Test environment configuration with isolated settings."""
    TESTING = True
    SECRET_KEY = "test-secret-key-for-unit-testing-v0.2"


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
