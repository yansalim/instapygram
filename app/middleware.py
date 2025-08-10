import os
import inspect
from functools import wraps
from flask import request
from .errors import UnauthorizedError, ForbiddenError


ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")


def admin_auth_required(fn):
    if inspect.iscoroutinefunction(fn):
        @wraps(fn)
        async def async_wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise UnauthorizedError("Token de autenticação ausente")
            token = auth_header.split(" ", 1)[1]
            if not ADMIN_TOKEN or token != ADMIN_TOKEN:
                raise ForbiddenError("Token inválido")
            return await fn(*args, **kwargs)

        return async_wrapper

    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise UnauthorizedError("Token de autenticação ausente")
        token = auth_header.split(" ", 1)[1]
        if not ADMIN_TOKEN or token != ADMIN_TOKEN:
            raise ForbiddenError("Token inválido")
        return fn(*args, **kwargs)

    return wrapper
