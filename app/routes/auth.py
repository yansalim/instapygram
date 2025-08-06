"""
Authentication endpoints.

This blueprint exposes endpoints for managing user sessions with
Instagram: logging in with username/password, resuming saved
sessions, checking session status, deleting sessions and importing
pre‑existing session JSON. Each view includes OpenAPI documentation
consumable by Flasgger to generate Swagger UI documentation.
"""
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, Unauthorized

from services.instagram_client import login_with_password, resume_session
from services.session_manager import (
    session_exists,
    delete_session,
    import_session_json,
)
from utils.validators import expect_json


# Blueprint instance for authentication routes
auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
@expect_json(["username", "password"])
def login():
    """Login with username and password.

    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - password
            properties:
              username:
                type: string
                example: conta_insta
              password:
                type: string
                example: minhasenha
              proxy:
                type: string
                nullable: true
                example: http://user:pass@host:port
    responses:
      200:
        description: Session created and serialized.
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                session:
                  type: object
      401:
        description: Authentication failure.
    """
    data = request.get_json()
    try:
        session = login_with_password(
            data["username"],
            data["password"],
            data.get("proxy"),
        )
        return jsonify({"message": "Login realizado", "session": session})
    except Exception as exc:
        # Convert any error to 401 to hide internal details
        raise Unauthorized(str(exc))


@auth_bp.route("/resume", methods=["POST"])
@expect_json(["username"])
def resume():
    """Resume an existing session from saved file.

    ---
    tags:
      - Auth
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
    responses:
      200:
        description: Session successfully resumed.
    """
    resume_session(request.get_json()["username"])
    return jsonify({"message": "Sessão retomada"})


@auth_bp.route("/status")
def status():
    """Check whether a session exists.

    ---
    tags:
      - Auth
    parameters:
      - in: query
        name: username
        schema:
          type: string
        required: true
    responses:
      200:
        description: Session status information.
    """
    username = request.args.get("username")
    if not username:
        raise BadRequest("username é obrigatório")
    return jsonify({"username": username, "active": session_exists(username)})


@auth_bp.route("/delete", methods=["DELETE"])
@expect_json(["username"])
def logout():
    """Delete a saved session.

    ---
    tags:
      - Auth
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
    responses:
      200:
        description: Session successfully deleted.
      400:
        description: Session not found.
    """
    if delete_session(request.get_json()["username"]):
        return jsonify({"message": "Sessão removida"})
    raise BadRequest("Sessão não encontrada")


@auth_bp.route("/login-session", methods=["POST"])
@expect_json(["username", "session"])
def login_session():
    """Import an already‑generated session JSON.

    ---
    tags:
      - Auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - username
              - session
            properties:
              username:
                type: string
              session:
                type: object
    responses:
      200:
        description: Session imported successfully.
    """
    body = request.get_json()
    import_session_json(body["username"], body["session"])
    return jsonify({"message": "Sessão importada"})