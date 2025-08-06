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
    # OpenAPI / Swagger configuration for Flasgger
    #
    # The Flasgger extension uses the values defined in this mapping to
    # generate the base OpenAPI specification.  By default Flasgger will
    # generate a Swagger 2.0 spec (i.e. include a top‑level ``swagger`` key).
    # However, this project defines its own OpenAPI 3.0 template in
    # ``app/swagger.py``.  To avoid mixing ``swagger`` and ``openapi`` keys in
    # the resulting document—which leads to the error shown in the Swagger UI
    # (“swagger and openapi fields cannot be present in the same definition”)—
    # we explicitly set ``openapi`` here.  When ``openapi`` is present,
    # Flasgger suppresses the default ``swagger`` key and uses the given
    # OpenAPI version instead.  The ``version`` field is informational and
    # should match the version specified in the template.
    SWAGGER = {
        "title": "Pipegram Flask API",
        # Use the Swagger UI v3 assets
        "uiversion": 3,
        # Force OpenAPI 3.x generation instead of Swagger 2.0
        "openapi": "3.0.3",
        # Application version exposed in the generated documentation
        "version": "1.0.0",
        # Optionally customise the route where the UI is served; Flasgger
        # defaults to ``/apidocs`` when unspecified.  Uncomment to change.
        # "specs_route": "/api-docs",
    }