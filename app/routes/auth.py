from flask import Blueprint, request, jsonify
from pydantic import BaseModel
from typing import Optional, Any, Dict
from ..errors import BadRequestError, ResourceNotFoundError
from ..services.instagram_client import login_with_password, resume_session
from ..utils import session_manager

bp = Blueprint("auth", __name__)

class LoginBody(BaseModel):
    username: str
    password: str
    proxy: Optional[str] = None

class ResumeBody(BaseModel):
    username: str

class StatusBody(BaseModel):
    username: str

class ImportBody(BaseModel):
    username: str
    session: Dict[str, Any]

@bp.post("/login")
async def login():
    """
    Login with Instagram
    ---
    tags: [Auth]
    summary: Login with Instagram credentials
    description: Authenticate a user using Instagram username and password
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Login credentials
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Instagram username
              example: "my_username"
            password:
              type: string
              description: Instagram account password
              example: "my_password123"
            proxy:
              type: string
              description: Optional proxy for connection
              example: "http://proxy:8080"
          required: 
            - username
            - password
    responses:
      200:
        description: Login successful
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Login successful"
            session:
              type: object
              description: Saved session data
      400:
        description: Authentication error
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Incorrect password"
    """
    body = LoginBody.model_validate(request.get_json(force=True))
    try:
        _, session = await login_with_password(body.username, body.password, body.proxy)
        return jsonify({"message": "Login successful", "session": session})
    except Exception as exc:
        error_msg = str(exc)
        if "checkpoint_challenge_required" in error_msg:
            return jsonify({"error": "Additional verification required (2FA/Captcha)"}), 400
        elif "bad_password" in error_msg:
            return jsonify({"error": "Incorrect password"}), 400
        elif "invalid_user" in error_msg:
            return jsonify({"error": "User not found"}), 400
        else:
            return jsonify({"error": f"Authentication failed: {error_msg}"}), 400

@bp.post("/resume")
async def resume():
    """
    Resume existing session
    ---
    tags: [Auth]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username: { type: string }
            required: [username]
    responses:
      200: { description: Session resumed }
    """
    body = ResumeBody.model_validate(request.get_json(force=True))
    try:
        await resume_session(body.username)
        return jsonify({"message": "Session resumed successfully"})
    except Exception:
        raise ResourceNotFoundError("Session not found or invalid")

@bp.get("/status")
def status():
    """
    Check session status
    ---
    tags: [Auth]
    parameters:
      - in: query
        name: username
        required: true
        schema: { type: string }
    responses:
      200: { description: Status returned }
    """
    username = request.args.get("username")
    if not username:
        raise BadRequestError("username is required")
    exists = session_manager.session_exists(username)
    return jsonify({"username": username, "status": "active" if exists else "not_found"})

@bp.delete("/delete")
def logout():
    """
    Delete saved session
    ---
    tags: [Auth]
    parameters:
      - in: query
        name: username
        required: true
        schema: { type: string }
    responses:
      200: { description: Session removed }
    """
    username = request.args.get("username")
    if not username:
        raise BadRequestError("username is required")
    success = session_manager.delete_session(username)
    if success:
        return jsonify({"message": "Session removed successfully"})
    raise ResourceNotFoundError("Session not found")

@bp.post("/import-session")
async def import_session():
    """
    Import existing session
    ---
    tags: [Auth]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username: { type: string, example: "my_username" }
              session: { type: object, description: "Complete exported session JSON" }
            required: [username, session]
    responses:
      200: { description: Session imported }
    """
    body = ImportBody.model_validate(request.get_json(force=True))
    try:
        session_manager.save_session(body.username, body.session)
        client = await resume_session(body.username)
        user = await client.current_user()
        return jsonify({"message": "Session imported successfully.", "logged_in_user": user})
    except Exception as exc:
        raise BadRequestError(f"Error importing session: {exc}")
