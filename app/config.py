"""
Application Configuration Module (v0.3 Secure Implementation)
Enforces secure session management, HTTP-only cookies, and configuration
policies.
"""

import os


class Config:
    """
    Base application configuration loaded from environment with fallbacks.
    """
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "v0.3-hardened-session-security-secret-key-24cys401"
    )
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "college_club.db")
    DEBUG = False
    TESTING = False

    # Session and Cookie Security Policies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes in seconds


class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Test environment configuration with isolated settings."""
    TESTING = True
    SECRET_KEY = os.environ.get(
        "TEST_SECRET_KEY", "testing-key-v0.3"
    )  # nosec B105
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
