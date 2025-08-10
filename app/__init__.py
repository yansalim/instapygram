from flask import Flask
from flasgger import Swagger
from asgiref.wsgi import WsgiToAsgi
from .errors import register_error_handlers


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.setdefault("SWAGGER", {
        "title": "Pipegram (Flask) - Instagram API",
        "uiversion": 3,
        "openapi": "3.0.0",
        "description": "API não oficial do Instagram usando instagrapi. Suporte completo a DMs, postagens, stories e mais.",
        "contact": {
            "name": "Pipegram Support",
            "url": "https://github.com/your-repo/pipegram"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        },
        "components": {
            "securitySchemes": {
                "bearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
            }
        },
        "security": [{"bearerAuth": []}],
    })
    Swagger(app)
    from .routes.auth import bp as auth_bp
    from .routes.post import bp as post_bp
    from .routes.dm import bp as dm_bp
    from .routes.profile import bp as profile_bp
    from .routes.stories import bp as stories_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(post_bp, url_prefix="/post")
    app.register_blueprint(dm_bp, url_prefix="/dm")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(stories_bp, url_prefix="/stories")
    @app.get("/")
    def root():
        return "🚀 API do Instagram não oficial (Flask + instagrapi) está rodando!"
    register_error_handlers(app)
    return app


# ASGI wrapper para Uvicorn
app = WsgiToAsgi(create_app())
