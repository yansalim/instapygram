"""
Blueprint registration.

This module centralises the import and registration of all API
blueprints. Each feature area of the API is isolated in its own
blueprint module, promoting modularity and separation of concerns.
"""


def register_blueprints(app):
    """Register all blueprints on the provided Flask app."""
    from .auth import auth_bp
    from .posts import posts_bp
    from .dm import dm_bp
    from .profile import profile_bp
    from .stories import stories_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(posts_bp, url_prefix="/post")
    app.register_blueprint(dm_bp, url_prefix="/dm")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(stories_bp, url_prefix="/stories")