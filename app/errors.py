"""
Centralised error handling.

This module provides functions for registering error handlers that
convert uncaught exceptions and HTTP exceptions into JSON responses.
By standardising error responses, clients can rely on consistent
error formats.
"""
from flask import jsonify
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):
    """Register handlers for HTTP and unhandled exceptions."""

    @app.errorhandler(HTTPException)
    def http_error(exc):
        # Render the error name and description as JSON
        response = {"error": exc.name, "description": exc.description}
        return jsonify(response), exc.code

    @app.errorhandler(Exception)
    def unhandled(exc):
        # Log the exception and hide internal details from the client
        app.logger.exception(exc)
        return jsonify({"error": "Internal Server Error"}), 500