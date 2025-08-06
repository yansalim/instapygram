"""
Decorators for request validation.

Provides a simple decorator to enforce that incoming requests contain
JSON bodies with required fields. If the body is missing or any
required fields are absent, a BadRequest exception is raised.
"""
from functools import wraps

from flask import request
from werkzeug.exceptions import BadRequest


def expect_json(required: list[str]):
    """Ensure that the request has JSON and required fields.

    Args:
        required: A list of field names that must be present in the
            request JSON body.

    Returns:
        A decorator to wrap Flask view functions.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                raise BadRequest("JSON esperado")
            data = request.get_json()
            missing = [fld for fld in required if fld not in data]
            if missing:
                raise BadRequest("Faltando: " + ", ".join(missing))
            return fn(*args, **kwargs)

        return wrapper

    return decorator