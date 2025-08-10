
from flask import Blueprint, request, jsonify
from pydantic import BaseModel
from typing import Optional
import base64
import requests
from ..errors import BadRequestError
from ..middleware import admin_auth_required
from ..services.instagram_client import resume_session

bp = Blueprint("post", __name__)

class PhotoFeedBody(BaseModel):
    username: str
    caption: str
    url: Optional[str] = None
    base64: Optional[str] = None

class PhotoStoryBody(BaseModel):
    username: str
    url: Optional[str] = None
    base64: Optional[str] = None

def buffer_from_source(b64: Optional[str], url: Optional[str]) -> bytes:
    if b64:
        try:
            data = b64.split(",", 1)[1] if "," in b64 else b64
            return base64.b64decode(data)
        except Exception as exc:
            raise BadRequestError(f"Erro ao decodificar base64: {exc}")
    if url:
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            return r.content
        except Exception as exc:
            raise BadRequestError(f"Erro ao baixar mídia da URL: {exc}")
    raise BadRequestError("Nem base64 nem url fornecidos.")

@bp.post("/photo-feed")
@admin_auth_required
async def post_photo_feed():
    """
    Publicar foto no feed
    ---
    tags: [Post]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username: { type: string, example: "minha_conta" }
              caption: { type: string, example: "Minha foto no feed!" }
              base64: { type: string }
              url: { type: string }
            required: [username, caption]
    responses:
      200: { description: Foto publicada com sucesso }
    """
    body = PhotoFeedBody.model_validate(request.get_json(force=True))
    try:
        if not body.base64 and not body.url:
            raise BadRequestError("Você deve informar ao menos base64 ou url")
        client = await resume_session(body.username)
        buffer = buffer_from_source(body.base64, body.url)
        result = await client.publish_photo(buffer, caption=body.caption)
        return jsonify({"message": "Foto publicada no Feed", "media": result})
    except Exception as exc:
        raise BadRequestError(str(exc))

@bp.post("/photo-story")
@admin_auth_required
async def post_photo_story():
    """
    Publicar foto nos Stories
    ---
    tags: [Post]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username: { type: string, example: "minha_conta" }
              base64: { type: string }
              url: { type: string }
            required: [username]
    responses:
      200: { description: Story com foto publicado }
    """
    body = PhotoStoryBody.model_validate(request.get_json(force=True))
    try:
        if not body.base64 and not body.url:
            raise BadRequestError("Você deve informar ao menos base64 ou url")
        client = await resume_session(body.username)
        buffer = buffer_from_source(body.base64, body.url)
        result = await client.publish_story_photo(buffer)
        return jsonify({"message": "Story publicado", "media": result})
    except Exception as exc:
        raise BadRequestError(str(exc))
