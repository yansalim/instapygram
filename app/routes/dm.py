"""
Direct Message endpoints.

This blueprint exposes endpoints for sending a simple text message to
another Instagram user, listing the inbox threads for the logged in
account and retrieving messages from a specific thread. All endpoints
require a valid admin token.
"""
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest

from utils.validators import expect_json
from utils.admin import admin_required
from services.instagram_client import get_client


dm_bp = Blueprint("dm", __name__)


@dm_bp.route("/send", methods=["POST"])
@admin_required
@expect_json(["username", "toUsername", "message"])
def send_dm():
    """Send a direct message to another user.

    ---
    tags:
      - DM
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
              - toUsername
              - message
            properties:
              username: {type: string}
              toUsername: {type: string}
              message: {type: string}
    responses:
      200:
        description: Message successfully sent. Returns the thread ID.
    """
    data = request.get_json()
    try:
        ig = get_client(data["username"])
        # Translate target username into numeric ID
        user_id = ig.user_id_from_username(data["toUsername"])
        thread_id = ig.direct_send(data["message"], user_ids=[user_id])
        return jsonify({"thread_id": thread_id})
    except Exception as exc:
        raise BadRequest(str(exc))


@dm_bp.route("/inbox", methods=["GET"])
@admin_required
def inbox():
    """List all direct message threads for the authenticated user.

    ---
    tags:
      - DM
    security:
      - bearerAuth: []
    parameters:
      - in: query
        name: username
        required: true
        schema:
          type: string
    responses:
      200:
        description: List of threads.
    """
    username = request.args.get("username")
    if not username:
        raise BadRequest("username é obrigatório")
    ig = get_client(username)
    return jsonify(ig.direct_threads())


@dm_bp.route("/thread/<thread_id>")
@admin_required
def thread(thread_id):
    """Retrieve messages from a specific thread.

    ---
    tags:
      - DM
    security:
      - bearerAuth: []
    parameters:
      - in: path
        name: thread_id
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
        description: List of messages in the thread.
    """
    username = request.args.get("username")
    if not username:
        raise BadRequest("username é obrigatório")
    ig = get_client(username)
    return jsonify(ig.direct_messages(thread_id))