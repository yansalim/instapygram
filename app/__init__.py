"""
Application factory and initialisation.

This module defines `create_app`, following the Flask application factory
pattern. It instantiates the Flask app, loads configuration, registers
extensions, sets up Swagger documentation, registers blueprints and
error handlers.
"""
from flask import Flask

from .config import Config
from .extensions import init_extensions
from .routes import register_blueprints
from .errors import register_error_handlers
from .swagger import init_swagger


def create_app() -> Flask:
    """Create and configure a new Flask application instance."""
    app = Flask(__name__)

    # Load config values from environment variables or defaults
    app.config.from_object(Config)

    # Initialise third‑party extensions (JWT, etc.)
    init_extensions(app)

    # Set up Swagger UI
    init_swagger(app)

    # Register blueprints for each API domain
    register_blueprints(app)

    # Register error handlers after blueprints
    register_error_handlers(app)

    return app