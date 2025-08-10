
from flask import Blueprint, request, jsonify
from pydantic import BaseModel
from typing import Optional
import base64
import requests
from ..errors import BadRequestError
from ..middleware import admin_auth_required
from ..services.instagram_client import resume_session

bp = Blueprint("profile", __name__)

class UpdateBioBody(BaseModel):
    username: str
    bio: Optional[str] = None
    url: Optional[str] = None
    base64: Optional[str] = None

class GetProfileBody(BaseModel):
    username: str

@bp.post("/update-bio")
@admin_auth_required
async def update_bio():
    """
    Atualizar bio e foto de perfil
    ---
    tags: [Profile]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username: { type: string }
              bio: { type: string, example: "Nova bio!" }
              url: { type: string }
              base64: { type: string }
            required: [username]
    responses:
      200: { description: Perfil atualizado com sucesso }
    """
    body = UpdateBioBody.model_validate(request.get_json(force=True))
    try:
        client = await resume_session(body.username)
        if body.bio:
            await client.edit_bio(body.bio)
        if body.base64 or body.url:
            if body.base64:
                data = base64.b64decode(body.base64.split(",", 1)[1] if "," in body.base64 else body.base64)
            else:
                resp = requests.get(body.url)
                resp.raise_for_status()
                data = resp.content
            await client.change_profile_picture(data)
        return jsonify({"message": "Bio e/ou foto de perfil atualizadas com sucesso"})
    except Exception as exc:
        raise BadRequestError(f"Erro ao atualizar bio/foto: {exc}")

@bp.get("/<targetUsername>")
@admin_auth_required
async def get_profile_by_username(targetUsername: str):
    """
    Buscar dados públicos de um perfil do Instagram
    ---
    tags: [Profile]
    parameters:
      - name: targetUsername
        in: path
        required: true
        schema: { type: string }
      - in: query
        name: username
        required: true
        schema: { type: string }
    responses:
      200: { description: Dados do perfil retornados com sucesso }
    """
    username = request.args.get("username")
    body = GetProfileBody.model_validate({"username": username})
    try:
        client = await resume_session(body.username)
        profile = await client.user_info(targetUsername)
        return jsonify(profile)
    except Exception as exc:
        raise BadRequestError(str(exc))
