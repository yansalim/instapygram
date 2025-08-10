from flask import Blueprint, request, jsonify
from pydantic import BaseModel, field_validator
from typing import Optional
import base64
import requests

from ..errors import BadRequestError
from ..middleware import admin_auth_required
from ..services.instagram_client import resume_session

bp = Blueprint("dm", __name__)

class SendDMBody(BaseModel):
    username: str
    toUsername: str
    message: str

class InboxBody(BaseModel):
    username: str

class SendPhotoDMBody(BaseModel):
    username: str
    toUsername: str
    url: Optional[str] = None
    base64: Optional[str] = None

    @field_validator("url")
    @classmethod
    def validate_input(cls, v, values):
        if (not v) and (not values.data.get("base64")):
            raise ValueError("Você deve informar ao menos base64 ou url")
        return v

@bp.post("/send")
@admin_auth_required
def send_text_dm():
    """
    Enviar DM de texto
    ---
    tags: [DM]
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username: { type: string, example: "minha_conta" }
              toUsername: { type: string, example: "destinatario" }
              message: { type: string, example: "Olá!" }
            required: [username, toUsername, message]
    responses:
      200: { description: DM enviada }
    """
    import asyncio
    body = SendDMBody.model_validate(request.get_json(force=True))
    try:
        client = asyncio.run(resume_session(body.username))
        asyncio.run(client.send_text_dm(body.toUsername, body.message))
        return jsonify({"message": "DM enviada"})
    except Exception as exc:
        raise BadRequestError(f"Erro ao enviar DM: {exc}")

@bp.get("/inbox")
@admin_auth_required
async def get_inbox():
    """
    Obter inbox de mensagens
    ---
    tags: [DM]
    security:
      - bearerAuth: []
    parameters:
      - in: query
        name: username
        required: true
        schema: { type: string }
    responses:
      200: { description: Inbox retornada }
    """
    username = request.args.get("username")
    if not username:
        raise BadRequestError("username é obrigatório")
    body = InboxBody.model_validate({"username": username})
    try:
        client = await resume_session(body.username)
        threads = await client.inbox()
        return jsonify(threads)
    except Exception as exc:
        raise BadRequestError(str(exc))

@bp.post("/send-photo")
@admin_auth_required
async def send_photo_dm():
    """
    Enviar imagem por DM (base64 ou URL)
    ---
    tags: [DM]
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username: { type: string, example: "minha_conta" }
              toUsername: { type: string, example: "destinatario" }
              base64: { type: string, example: "data:image/jpeg;base64,/9j/4AA..." }
              url: { type: string, example: "https://exemplo.com/imagem.jpg" }
            required: [username, toUsername]
    responses:
      200: { description: Imagem enviada por DM }
    """
    body = SendPhotoDMBody.model_validate(request.get_json(force=True))
    try:
        client = await resume_session(body.username)
        if body.url:
            resp = requests.get(body.url)
            resp.raise_for_status()
            await client.send_photo_dm_from_bytes(body.toUsername, resp.content)
        else:
            data_str = body.base64.split(",", 1)[1] if "," in body.base64 else body.base64
            data = base64.b64decode(data_str)
            await client.send_photo_dm_from_bytes(body.toUsername, data)
        return jsonify({"message": "Imagem enviada com sucesso"})
    except Exception as exc:
        raise BadRequestError(f"Erro ao enviar imagem por DM: {exc}")

@bp.get("/thread/<threadId>")
@admin_auth_required
async def get_thread_messages(threadId: str):
    """
    Obter mensagens da conversa
    ---
    tags: [DM]
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: threadId
        required: true
        schema: { type: string }
        example: "12345678901234567"
      - in: query
        name: username
        required: true
        schema: { type: string }
    responses:
      200: { description: Mensagens retornadas }
    """
    username = request.args.get("username")
    if not username:
        raise BadRequestError("username é obrigatório")
    try:
        client = await resume_session(username)
        messages = await client.thread_messages(threadId.strip())
        return jsonify(messages)
    except Exception as exc:
        raise BadRequestError(f"Erro ao buscar mensagens da thread {threadId}: {exc}")
