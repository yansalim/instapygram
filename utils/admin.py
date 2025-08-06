"""
Authentication helpers for admin routes.

Provides a decorator to enforce that the request includes a valid
Bearer token matching the ADMIN_TOKEN configured for the application.
If no Authorization header is provided or the token does not match,
appropriate HTTP exceptions are raised.
"""
from functools import wraps
from flask import request, current_app
from werkzeug.exceptions import Unauthorized, Forbidden


def admin_required(fn):
    """Decorator to enforce admin authentication via Bearer token.

    This decorator expects the client to send an Authorization header
    with the form `Bearer <token>`. The token is compared with the
    `ADMIN_TOKEN` configured in the Flask application. If the header
    is missing or the token does not match, it raises `Unauthorized`
    or `Forbidden`, respectively.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise Unauthorized("Token de autenticação ausente")
        token = auth_header.split()[1]
        expected = current_app.config.get("ADMIN_TOKEN")
        if token != expected:
            raise Forbidden("Token inválido")
        return fn(*args, **kwargs)

    return wrapper