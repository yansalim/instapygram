from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    # Swagger configuration (adjust according to your setup)
    app.config["SWAGGER"] = {
        "title": "Pipegram (Flask) - Instagram API",
        "uiversion": 3,
        "swagger": "2.0",
        "version": "1.0.0",
        "description": "Unofficial Instagram API using instagrapi. Complete support for DMs, posts, stories and more.",
        "contact": {
            "name": "Pipegram Support",
            "url": "https://github.com/your-repo/pipegram"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        },
        "host": "localhost:3000",
        "basePath": "/",
        "schemes": ["http"],
        "securityDefinitions": {
            "bearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Authentication token to access protected routes. Use: Bearer token"
            }
        },

        "security": [
            {
                "bearerAuth": []
            }
        ],
        "tags": [
            {
                "name": "Auth",
                "description": "Authentication operations"
            },
            {
                "name": "DM",
                "description": "Direct message operations"
            },
            {
                "name": "Post",
                "description": "Post operations"
            },
            {
                "name": "Profile",
                "description": "Profile operations"
            },
            {
                "name": "Stories",
                "description": "Story operations"
            }
        ]
    }
    Swagger(app)

    # Root route for testing
    @app.route("/")
    def root():
        return "🚀 Unofficial Instagram API (Flask) is running!"

    # Import and register blueprints
    from .routes import auth, post, profile, stories, dm

    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(post.bp, url_prefix="/post")
    app.register_blueprint(profile.bp, url_prefix="/profile")
    app.register_blueprint(stories.bp, url_prefix="/stories")
    app.register_blueprint(dm.bp, url_prefix="/dm")

    # Register error handlers
    from .errors import register_error_handlers
    register_error_handlers(app)

    # Global middlewares, handlers, etc. (if any)
    return app

# Create Flask application
app = create_app()
