
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
    summary: Publish photo to Instagram feed
    description: Publishes a photo to the Instagram feed using base64 or URL
    security:
      - bearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Photo data (base64 or URL)
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Username of the account that will publish the photo
              example: "my_account"
            caption:
              type: string
              description: Caption for the photo
              example: "My photo in the feed!"
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
            - caption
    responses:
      200:
        description: Photo published successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Photo published to Feed"
            media:
              type: object
              description: Published media information
      400:
        description: Error publishing photo
        schema:
          type: object
          properties:
            error:
              type: string
              example: "You must provide either base64 or url"
      401:
        description: Missing or invalid authentication token
      403:
        description: Invalid token
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
    summary: Publish photo to Instagram Stories
    description: Publishes a photo to Instagram Stories using base64 or URL
    security:
      - bearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Photo data (base64 or URL)
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Username of the account that will publish the story
              example: "my_account"
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
    responses:
      200:
        description: Story with photo published
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Story published"
            media:
              type: object
              description: Published media information
      400:
        description: Error publishing story
        schema:
          type: object
          properties:
            error:
              type: string
              example: "You must provide either base64 or url"
      401:
        description: Missing or invalid authentication token
      403:
        description: Invalid token
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
