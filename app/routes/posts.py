"""
Endpoints for publishing media to Instagram.

This blueprint handles uploading photos and videos to feed, stories
and reels. All endpoints require a valid admin token and accept
either a URL or a Base64 encoded payload to obtain the media
contents. Each endpoint is documented for Swagger via Flasgger
docstrings.
"""
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest

from utils.validators import expect_json
from utils.media import get_buffer_from_source
from utils.admin import admin_required
from services.instagram_client import get_client


posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/photo-feed", methods=["POST"])
@admin_required
@expect_json(["username", "caption"])
def photo_feed():
    """Publish a photo to the feed.

    ---
    tags:
      - Posts
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - caption
            properties:
              username:
                type: string
              caption:
                type: string
              url:
                type: string
                nullable: true
              base64:
                type: string
                nullable: true
    responses:
      200:
        description: Photo successfully published.
    """
    data = request.get_json()
    buffer = get_buffer_from_source(data)
    try:
        ig = get_client(data["username"])
        media = ig.photo_upload(buffer, data["caption"])
        return jsonify({"message": "Foto publicada", "media": media.dict()})
    except Exception as exc:
        raise BadRequest(str(exc))


@posts_bp.route("/photo-story", methods=["POST"])
@admin_required
@expect_json(["username"])
def photo_story():
    """Publish a photo to stories.

    ---
    tags:
      - Posts
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
            properties:
              username:
                type: string
              url:
                type: string
                nullable: true
              base64:
                type: string
                nullable: true
    responses:
      200:
        description: Story successfully published.
    """
    data = request.get_json()
    buffer = get_buffer_from_source(data)
    try:
        ig = get_client(data["username"])
        media = ig.photo_upload_to_story(buffer)
        return jsonify({"message": "Story publicado", "media": media.dict()})
    except Exception as exc:
        raise BadRequest(str(exc))


@posts_bp.route("/video-feed", methods=["POST"])
@admin_required
@expect_json(["username", "caption"])
def video_feed():
    """Publish a video to the feed.

    ---
    tags:
      - Posts
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - caption
            properties:
              username:
                type: string
              caption:
                type: string
              url:
                type: string
                nullable: true
              base64:
                type: string
                nullable: true
    responses:
      200:
        description: Video successfully published.
    """
    data = request.get_json()
    buffer = get_buffer_from_source(data)
    try:
        ig = get_client(data["username"])
        media = ig.video_upload(buffer, data["caption"])
        return jsonify({"message": "Vídeo publicado", "media": media.dict()})
    except Exception as exc:
        raise BadRequest(str(exc))


@posts_bp.route("/video-story", methods=["POST"])
@admin_required
@expect_json(["username"])
def video_story():
    """Publish a video to stories.

    ---
    tags:
      - Posts
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
            properties:
              username:
                type: string
              url:
                type: string
                nullable: true
              base64:
                type: string
                nullable: true
    responses:
      200:
        description: Video story successfully published.
    """
    data = request.get_json()
    buffer = get_buffer_from_source(data)
    try:
        ig = get_client(data["username"])
        media = ig.video_upload_to_story(buffer)
        return jsonify({"message": "Vídeo Story publicado", "media": media.dict()})
    except Exception as exc:
        raise BadRequest(str(exc))


@posts_bp.route("/video-reels", methods=["POST"])
@admin_required
@expect_json(["username", "caption"])
def video_reels():
    """Publish a video reel.

    ---
    tags:
      - Posts
    security:
      - bearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - caption
            properties:
              username:
                type: string
              caption:
                type: string
              url:
                type: string
                nullable: true
              base64:
                type: string
                nullable: true
    responses:
      200:
        description: Reel successfully published.
    """
    data = request.get_json()
    buffer = get_buffer_from_source(data)
    try:
        ig = get_client(data["username"])
        media = ig.video_upload(
            buffer,
            data["caption"],
            to_feed=False,
            to_reel=True,
        )
        return jsonify({"message": "Reel publicado", "media": media.dict()})
    except Exception as exc:
        raise BadRequest(str(exc))