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
    Login com Instagram
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
              password: { type: string }
              proxy: { type: string }
            required: [username, password]
    responses:
      200: { description: Login realizado com sucesso }
    """
    body = LoginBody.model_validate(request.get_json(force=True))
    try:
        _, session = await login_with_password(body.username, body.password, body.proxy)
        return jsonify({"message": "Login realizado com sucesso", "session": session})
    except Exception as exc:
        error_msg = str(exc)
        if "checkpoint_challenge_required" in error_msg:
            return jsonify({"error": "Verificação adicional necessária (2FA/Captcha)"}), 400
        elif "bad_password" in error_msg:
            return jsonify({"error": "Senha incorreta"}), 400
        elif "invalid_user" in error_msg:
            return jsonify({"error": "Usuário não encontrado"}), 400
        else:
            return jsonify({"error": f"Falha ao autenticar: {error_msg}"}), 400

@bp.post("/resume")
async def resume():
    """
    Retomar sessão existente
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
      200: { description: Sessão retomada }
    """
    body = ResumeBody.model_validate(request.get_json(force=True))
    try:
        await resume_session(body.username)
        return jsonify({"message": "Sessão retomada com sucesso"})
    except Exception:
        raise ResourceNotFoundError("Sessão não encontrada ou inválida")

@bp.get("/status")
def status():
    """
    Verificar status de sessão
    ---
    tags: [Auth]
    parameters:
      - in: query
        name: username
        required: true
        schema: { type: string }
    responses:
      200: { description: Status retornado }
    """
    username = request.args.get("username")
    if not username:
        raise BadRequestError("username é obrigatório")
    exists = session_manager.session_exists(username)
    return jsonify({"username": username, "status": "ativa" if exists else "inexistente"})

@bp.delete("/delete")
def logout():
    """
    Excluir sessão salva
    ---
    tags: [Auth]
    parameters:
      - in: query
        name: username
        required: true
        schema: { type: string }
    responses:
      200: { description: Sessão removida }
    """
    username = request.args.get("username")
    if not username:
        raise BadRequestError("username é obrigatório")
    success = session_manager.delete_session(username)
    if success:
        return jsonify({"message": "Sessão removida com sucesso"})
    raise ResourceNotFoundError("Sessão não encontrada")

@bp.post("/import-session")
async def import_session():
    """
    Importar sessão existente
    ---
    tags: [Auth]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              username: { type: string, example: "meu_usuario" }
              session: { type: object, description: "JSON completo da sessão exportada" }
            required: [username, session]
    responses:
      200: { description: Sessão importada }
    """
    body = ImportBody.model_validate(request.get_json(force=True))
    try:
        session_manager.save_session(body.username, body.session)
        client = await resume_session(body.username)
        user = await client.current_user()
        return jsonify({"message": "Sessão importada com sucesso.", "logged_in_user": user})
    except Exception as exc:
        raise BadRequestError(f"Erro ao importar sessão: {exc}")
