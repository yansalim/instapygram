"""
Profile endpoints.

This blueprint defines endpoints to retrieve public profile details
about a given username and to update the biography and/or profile
picture of the logged in user. All endpoints require a valid admin
token.
"""
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest

from utils.validators import expect_json
from utils.media import get_buffer_from_source
from utils.admin import admin_required
from services.instagram_client import get_client


profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/<target_username>", methods=["GET"])
@admin_required
def public_profile(target_username):
    """Get the public profile information of another user.

    ---
    tags:
      - Profile
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: target_username
        required: true
        schema:
          type: string
      - in: query
        name: username
        required: true
        schema:
          type: string
    responses:
      200:
        description: The user information.
    """
    username = request.args.get("username")
    if not username:
        raise BadRequest("username é obrigatório")
    ig = get_client(username)
    info = ig.user_info_by_username(target_username)
    return jsonify(info.dict())


@profile_bp.route("/update-bio", methods=["POST"])
@admin_required
@expect_json(["username"])
def update_bio():
    """Update the biography and/or profile picture of the logged in user.

    ---
    tags:
      - Profile
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
              bio:
                type: string
                nullable: true
              url:
                type: string
                nullable: true
              base64:
                type: string
                nullable: true
    responses:
      200:
        description: Profile successfully updated.
    """
    data = request.get_json()
    ig = get_client(data["username"])
    # Update biography if provided
    if bio := data.get("bio"):
        ig.account_edit(biography=bio)
    # Update profile picture if a media payload is provided
    if data.get("base64") or data.get("url"):
        buffer = get_buffer_from_source(data)
        ig.account_change_picture(buffer)
    return jsonify({"message": "Perfil atualizado"})