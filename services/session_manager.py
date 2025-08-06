"""
Persistence of session settings.

All sessions are saved to the local filesystem as JSON files within
the `sessions` directory. The filename is derived from the username
to which the session belongs. This module provides helper functions
to save, load, check for the existence of and delete sessions.
"""
import json
from pathlib import Path


SESSION_DIR = Path("sessions")
SESSION_DIR.mkdir(exist_ok=True)


def _path(username: str) -> Path:
    """Return the path on disk for a given username's session."""
    return SESSION_DIR / f"{username}.json"


def save_session(username: str, session: dict):
    """Persist the provided session settings to disk."""
    _path(username).write_text(json.dumps(session))


def load_session(username: str):
    """Load the session settings for the specified username.

    Raises FileNotFoundError if the session file does not exist.
    """
    path = _path(username)
    if not path.exists():
        raise FileNotFoundError(f"Sessão não encontrada: {username}")
    return json.loads(path.read_text())


def delete_session(username: str) -> bool:
    """Remove the session file for the given username if it exists.

    Returns True if a file was removed, False otherwise.
    """
    p = _path(username)
    if p.exists():
        p.unlink()
        return True
    return False


def session_exists(username: str) -> bool:
    """Return True if a session exists for the provided username."""
    return _path(username).exists()


def import_session_json(username: str, session_json: dict):
    """Import raw session JSON into a session file.

    This helper simply forwards to `save_session` for clarity.
    """
    save_session(username, session_json)