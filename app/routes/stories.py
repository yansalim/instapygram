"""
Story endpoints.

This blueprint exposes a single endpoint for retrieving the current
public stories of a given user. A valid admin token is required.
"""
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest

from utils.validators import expect_json
from utils.admin import admin_required
from services.instagram_client import get_client


stories_bp = Blueprint("stories", __name__)


@stories_bp.route("/", methods=["POST"])
@admin_required
@expect_json(["username", "targetUsername"])
def get_user_stories():
    """Retrieve the current stories of a public user.

    ---
    tags:
      - Stories
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
              - targetUsername
            properties:
              username:
                type: string
              targetUsername:
                type: string
    responses:
      200:
        description: List of stories.
    """
    data = request.get_json()
    ig = get_client(data["username"])
    try:
        # Convert the target username into a numeric ID
        user_id = ig.user_id_from_username(data["targetUsername"])
        stories = [item.dict() for item in ig.user_stories(user_id)]
        return jsonify(stories)
    except Exception as exc:
        raise BadRequest(str(exc))