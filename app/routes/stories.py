
from flask import Blueprint, request, jsonify
from pydantic import BaseModel
from ..errors import BadRequestError
from ..middleware import admin_auth_required
from ..services.instagram_client import resume_session

bp = Blueprint("stories", __name__)

class StoriesBody(BaseModel):
    username: str
    targetUsername: str

@bp.get("/")
@admin_auth_required
async def get_user_stories():
    """
    Listar stories de um usuário
    ---
    tags: [Stories]
    parameters:
      - in: query
        name: username
        required: true
        schema: { type: string }
      - in: query
        name: targetUsername
        required: true
        schema: { type: string }
    responses:
      200: { description: Stories obtidos com sucesso }
    """
    body = StoriesBody.model_validate({
        "username": request.args.get("username"),
        "targetUsername": request.args.get("targetUsername"),
    })
    try:
        client = await resume_session(body.username)
        items = await client.user_stories(body.targetUsername)
        return jsonify(items)
    except Exception as exc:
        raise BadRequestError(str(exc))
