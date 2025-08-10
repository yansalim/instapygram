
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
            raise BadRequestError(f"Error decoding base64: {exc}")
    if url:
        try:
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            r.raise_for_status()
            return r.content
        except Exception as exc:
            raise BadRequestError(f"Error downloading media from URL: {exc}")
    raise BadRequestError("Neither base64 nor url provided.")

@bp.post("/photo-feed")
@admin_auth_required
async def post_photo_feed():
    """
    Publish photo to feed
    ---
    tags: [Post]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username: { type: string, example: "my_account" }
              caption: { type: string, example: "My photo in the feed!" }
              base64: { type: string }
              url: { type: string }
            required: [username, caption]
    responses:
      200: { description: Photo published successfully }
    """
    body = PhotoFeedBody.model_validate(request.get_json(force=True))
    try:
        if not body.base64 and not body.url:
            raise BadRequestError("You must provide either base64 or url")
        client = await resume_session(body.username)
        buffer = buffer_from_source(body.base64, body.url)
        result = await client.publish_photo(buffer, caption=body.caption)
        return jsonify({"message": "Photo published to Feed", "media": result})
    except Exception as exc:
        raise BadRequestError(str(exc))

@bp.post("/photo-story")
@admin_auth_required
async def post_photo_story():
    """
    Publish photo to Stories
    ---
    tags: [Post]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username: { type: string, example: "my_account" }
              base64: { type: string }
              url: { type: string }
            required: [username]
    responses:
      200: { description: Story with photo published }
    """
    body = PhotoStoryBody.model_validate(request.get_json(force=True))
    try:
        if not body.base64 and not body.url:
            raise BadRequestError("You must provide either base64 or url")
        client = await resume_session(body.username)
        buffer = buffer_from_source(body.base64, body.url)
        result = await client.publish_story_photo(buffer)
        return jsonify({"message": "Story published", "media": result})
    except Exception as exc:
        raise BadRequestError(str(exc))
