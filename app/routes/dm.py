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
            raise ValueError("You must provide either base64 or url")
        return v

@bp.post("/send")
@admin_auth_required
def send_text_dm():
    """
    Send text DM
    ---
    tags: [DM]
    summary: Send text message via DM
    description: Sends a text message to a specific user
    security:
      - bearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Message data
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Username of the account that will send the message
              example: "my_account"
            toUsername:
              type: string
              description: Recipient username
              example: "recipient"
            message:
              type: string
              description: Message to be sent
              example: "Hello! How are you?"
          required: 
            - username
            - toUsername
            - message
    responses:
      200:
        description: DM sent successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "DM sent"
      400:
        description: Error sending DM
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error sending DM: Session not found"
      401:
        description: Missing or invalid authentication token
      403:
        description: Invalid token
    """
    import asyncio
    body = SendDMBody.model_validate(request.get_json(force=True))
    try:
        client = asyncio.run(resume_session(body.username))
        asyncio.run(client.send_text_dm(body.toUsername, body.message))
        return jsonify({"message": "DM sent"})
    except Exception as exc:
        raise BadRequestError(f"Error sending DM: {exc}")

@bp.get("/inbox")
@admin_auth_required
async def get_inbox():
    """
    Get message inbox
    ---
    tags: [DM]
    summary: List inbox conversations
    description: Returns all direct message conversations
    security:
      - bearerAuth: []
    produces:
      - application/json
    parameters:
      - in: query
        name: username
        required: true
        type: string
        description: Account username
        example: "my_account"
    responses:
      200:
        description: Conversation list returned
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
                example: "Conversation with @user"
              users:
                type: array
                items:
                  type: object
                  properties:
                    username:
                      type: string
                      example: "user"
                    full_name:
                      type: string
                      example: "Full Name"
                    profile_pic_url:
                      type: string
                      example: "https://example.com/photo.jpg"
              last_message:
                type: string
                example: "Last message in conversation"
              last_message_timestamp:
                type: string
                example: "2025-08-10T18:00:00Z"
      400:
        description: Request error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "username is required"
      401:
        description: Missing or invalid authentication token
      403:
        description: Invalid token
    """
    username = request.args.get("username")
    if not username:
        raise BadRequestError("username is required")
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
    Send image via DM (base64 or URL)
    ---
    tags: [DM]
    summary: Send photo via direct message
    description: Sends an image via DM using base64 or URL
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
                description: Username of the account that will send the photo
                example: "my_account"
              toUsername:
                type: string
                description: Recipient username
                example: "recipient"
              base64:
                type: string
                description: Image in base64 format (data:image/jpeg;base64,...)
                example: "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
              url:
                type: string
                description: Image URL for download
                example: "https://example.com/image.jpg"
            required: 
              - username
              - toUsername
    responses:
      200:
        description: Image sent successfully
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Image sent successfully"
      400:
        description: Error sending image
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Error sending image via DM: Invalid URL"
      401:
        description: Missing or invalid authentication token
      403:
        description: Invalid token
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
        return jsonify({"message": "Image sent successfully"})
    except Exception as exc:
        raise BadRequestError(f"Error sending image via DM: {exc}")

@bp.get("/thread/<threadId>")
@admin_auth_required
async def get_thread_messages(threadId: str):
    """
    Get conversation messages
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
      200: { description: Messages returned }
    """
    username = request.args.get("username")
    if not username:
        raise BadRequestError("username is required")
    try:
        client = await resume_session(username)
        messages = await client.thread_messages(threadId.strip())
        return jsonify(messages)
    except Exception as exc:
        raise BadRequestError(f"Error fetching thread messages {threadId}: {exc}")
