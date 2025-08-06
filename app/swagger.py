"""
Swagger configuration using Flasgger.

Initialises the Swagger UI and defines a base OpenAPI template
containing meta data, servers and tags. Flasgger reads the
docstrings on each route to populate the endpoint definitions.
"""
from flasgger import Swagger


def init_swagger(app):
    """Initialise the Swagger UI with a base template."""
    template = {
        "openapi": "3.0.3",
        "info": {
            "title": "Pipegram Flask API",
            "version": "1.0.0",
            "description": (
                "API não-oficial do Instagram reimplementada em Flask. "
                "Permite publicar no feed, stories e reels, enviar mensagens diretas "
                "e recuperar informações de perfil e stories."
            ),
        },
        "servers": [{"url": "/"}],
        "tags": [
            {"name": "Auth", "description": "Autenticação e sessões"},
            {"name": "Posts", "description": "Postagens (feed, stories, reels)"},
            {"name": "DM", "description": "Direct Messages"},
            {"name": "Profile", "description": "Operações de perfil"},
            {"name": "Stories", "description": "Recuperação de stories públicos"},
        ],
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "Forneça o token ADMIN via header Authorization: Bearer <token>",
                }
            }
        },
    }
    Swagger(app, template=template)