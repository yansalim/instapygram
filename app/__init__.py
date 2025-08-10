from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    # Config Swagger (ajuste conforme seu setup)
    app.config["SWAGGER"] = {
        "title": "Pipegram (Flask) - Instagram API",
        "uiversion": 3,
        "swagger": "2.0",
        "version": "1.0.0",
        "description": "API não oficial do Instagram usando instagrapi. Suporte completo a DMs, postagens, stories e mais.",
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
                "description": "Token de autenticação para acessar as rotas protegidas. Use: Bearer token"
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
                "description": "Operações de autenticação"
            },
            {
                "name": "DM",
                "description": "Operações de mensagens diretas"
            },
            {
                "name": "Post",
                "description": "Operações de postagens"
            },
            {
                "name": "Profile",
                "description": "Operações de perfil"
            },
            {
                "name": "Stories",
                "description": "Operações de stories"
            }
        ]
    }
    Swagger(app)

    # Rota raiz para teste
    @app.route("/")
    def root():
        return "🚀 API do Instagram não oficial (Flask) está rodando!"

    # Importa e registra blueprints
    from .routes import auth, post, profile, stories, dm

    app.register_blueprint(auth.bp, url_prefix="/auth")
    app.register_blueprint(post.bp, url_prefix="/post")
    app.register_blueprint(profile.bp, url_prefix="/profile")
    app.register_blueprint(stories.bp, url_prefix="/stories")
    app.register_blueprint(dm.bp, url_prefix="/dm")

    # Registrar handlers de erro
    from .errors import register_error_handlers
    register_error_handlers(app)

    # Middlewares globais, handlers etc. (se houver)
    return app

# Criar a aplicação Flask
app = create_app()
