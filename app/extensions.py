"""
Third‑party extension initialisation.

This module defines global instances of extensions (e.g. JWTManager) and
provides a helper to bind them to a Flask app. Centralising extension
initialisation in this module prevents circular imports.
"""
from flask_jwt_extended import JWTManager

# Create extension instances
jwt = JWTManager()


def init_extensions(app):
    """Bind extensions to the Flask application instance."""
    # At the moment only JWTManager is initialised. Additional extensions
    # (e.g. database, marshmallow) can be added here later.
    jwt.init_app(app)