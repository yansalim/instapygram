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
    summary: Enviar mensagem de texto por DM
    description: Envia uma mensagem de texto para um usuário específico
    security:
      - bearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Dados da mensagem
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Nome de usuário da conta que enviará a mensagem
              example: "minha_conta"
            toUsername:
              type: string
              description: Nome de usuário do destinatário
              example: "destinatario"
            message:
              type: string
              description: Mensagem a ser enviada
              example: "Olá! Como você está?"
          required: 
            - username
            - toUsername
            - message
    responses:
      200:
        description: DM enviada com sucesso
        schema:
          type: object
          properties:
            message:
              type: string
              example: "DM enviada"
      400:
        description: Erro ao enviar DM
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro ao enviar DM: Sessão não encontrada"
      401:
        description: Token de autenticação ausente ou inválido
      403:
        description: Token inválido
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
    summary: Listar conversas do inbox
    description: Retorna todas as conversas de mensagens diretas
    security:
      - bearerAuth: []
    produces:
      - application/json
    parameters:
      - in: query
        name: username
        required: true
        type: string
        description: Nome de usuário da conta
        example: "minha_conta"
    responses:
      200:
        description: Lista de conversas retornada
        schema:
          type: array
          items:
            type: object
            properties:
              thread_id:
                type: string
                example: "12345678901234567"
              thread_title:
                type: string
                example: "Conversa com @usuario"
              users:
                type: array
                items:
                  type: object
                  properties:
                    username:
                      type: string
                      example: "usuario"
                    full_name:
                      type: string
                      example: "Nome Completo"
                    profile_pic_url:
                      type: string
                      example: "https://example.com/photo.jpg"
              last_message:
                type: string
                example: "Última mensagem da conversa"
              last_message_timestamp:
                type: string
                example: "2025-08-10T18:00:00Z"
      400:
        description: Erro na requisição
        schema:
          type: object
          properties:
            error:
              type: string
              example: "username é obrigatório"
      401:
        description: Token de autenticação ausente ou inválido
      403:
        description: Token inválido
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
    summary: Enviar foto por mensagem direta
    description: Envia uma imagem por DM usando base64 ou URL
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username:
                type: string
                description: Nome de usuário da conta que enviará a foto
                example: "minha_conta"
              toUsername:
                type: string
                description: Nome de usuário do destinatário
                example: "destinatario"
              base64:
                type: string
                description: Imagem em formato base64 (data:image/jpeg;base64,...)
                example: "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
              url:
                type: string
                description: URL da imagem para download
                example: "https://exemplo.com/imagem.jpg"
            required: 
              - username
              - toUsername
    responses:
      200:
        description: Imagem enviada com sucesso
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Imagem enviada com sucesso"
      400:
        description: Erro ao enviar imagem
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Erro ao enviar imagem por DM: URL inválida"
      401:
        description: Token de autenticação ausente ou inválido
      403:
        description: Token inválido
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
