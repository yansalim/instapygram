"""
Application configuration.

All configurable options are defined in this class. Values are loaded
from environment variables when available, falling back to sensible
defaults.  This module also defines the Swagger configuration used by
Flasgger.
"""
import os
from datetime import timedelta


class Config:
    """Base configuration class for the Flask application."""

    # Secret used for Flask session cookies
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_me")
    # Token required in the Authorization header for privileged routes
    ADMIN_TOKEN: str = os.getenv("ADMIN_TOKEN", "supersecret")

    # Flask general options
    JSON_SORT_KEYS: bool = False
    MAX_CONTENT_LENGTH: int = 100 * 1024 * 1024  # 100 MB upload limit

    # JSON Web Token settings (if you choose to use JWT in the future)
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "jwt_change_me")
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(hours=12)

    # Swagger / Flasgger settings
    SWAGGER = {
        "title": "Pipegram Flask API",
        "uiversion": 3,
    }