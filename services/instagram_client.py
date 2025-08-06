"""
Service wrapper around the instagrapi Client.

This module encapsulates the interactions with the unofficial
Instagram API provided by `instagrapi`. It provides helper
functions for logging in, resuming sessions and retrieving
client instances bound to stored sessions. To minimise overhead,
deserialised clients are cached using `functools.lru_cache`.
"""
from functools import lru_cache

from instagrapi import Client

from .session_manager import save_session, load_session


def _prepare_client() -> Client:
    """Initialise a new Client with reasonable defaults."""
    ig = Client()
    # Delay requests to mimic human behaviour and reduce rate limiting
    ig.delay_range = [2, 4]
    return ig


def login_with_password(username: str, password: str, proxy: str | None = None):
    """Authenticate with Instagram using username and password.

    If a proxy is provided, the client will route requests through it.
    The session settings are saved to disk for later reuse.
    """
    ig = _prepare_client()
    if proxy:
        ig.set_proxy(proxy)
    ig.login(username, password)
    save_session(username, ig.get_settings())
    return ig.get_settings()


@lru_cache(maxsize=32)
def get_client(username: str) -> Client:
    """Return a Client instance configured with the stored session for `username`.

    The client is cached to avoid repeatedly deserialising session settings.
    An exception is raised if no session exists for the provided username.
    """
    settings = load_session(username)
    ig = _prepare_client()
    ig.set_settings(settings)
    return ig


def resume_session(username: str):
    """Ensure that a stored session is valid.

    Attempt to call an innocuous endpoint (`get_timeline_feed`) to
    verify that the session still works. If it fails, an exception
    will be propagated to the caller.
    """
    # Just call get_client to load and cache the client; then perform a test call
    client = get_client(username)
    # Validate by making a harmless call
    client.get_timeline_feed()