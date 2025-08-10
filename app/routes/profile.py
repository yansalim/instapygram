
from flask import Blueprint, request, jsonify
from pydantic import BaseModel, model_validator
from typing import Optional
import base64
import requests
from ..errors import BadRequestError
from ..middleware import admin_auth_required
from ..services.instagram_client import resume_session

bp = Blueprint("profile", __name__)

class UpdateBioBody(BaseModel):
    username: str
    bio: Optional[str] = None
    url: Optional[str] = None
    base64: Optional[str] = None

    @model_validator(mode='after')
    def validate_at_least_one_field(self):
        if not any([self.bio, self.url, self.base64]):
            raise ValueError("At least one field (bio, url, or base64) must be provided")
        return self

class GetProfileBody(BaseModel):
    username: str

@bp.post("/update-bio")
@admin_auth_required
async def update_bio():
    """
    Update bio and profile picture
    ---
    tags: [Profile]
    summary: Update Instagram bio and profile picture
    description: Updates the bio text and/or profile picture using base64 or URL. At least one field (bio, base64, or url) must be provided along with username.
    security:
      - bearerAuth: []
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        description: Profile update data (bio and/or picture). At least one field (bio, base64, or url) must be provided.
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Username of the account to update (required)
              example: "my_account"
            bio:
              type: string
              description: New bio text (optional)
              example: "New bio!"
            base64:
              type: string
              description: Profile picture in base64 format (optional)
              example: "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
            url:
              type: string
              description: Profile picture URL for download (optional)
              example: "https://example.com/profile.jpg"
          required: 
            - username
    responses:
      200:
        description: Profile updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Bio and/or profile picture updated successfully"
      400:
        description: Error updating profile
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error updating bio/picture: Session not found"
      401:
        description: Missing or invalid authentication token
      403:
        description: Invalid token
    """
    body = UpdateBioBody.model_validate(request.get_json(force=True))
    try:
        client = await resume_session(body.username)
        if body.bio:
            await client.edit_bio(body.bio)
        if body.base64 or body.url:
            if body.base64:
                data = base64.b64decode(body.base64.split(",", 1)[1] if "," in body.base64 else body.base64)
            else:
                resp = requests.get(body.url)
                resp.raise_for_status()
                data = resp.content
            await client.change_profile_picture(data)
        return jsonify({"message": "Bio and/or profile picture updated successfully"})
    except Exception as exc:
        raise BadRequestError(f"Error updating bio/picture: {exc}")

@bp.get("/<targetUsername>")
@admin_auth_required
async def get_profile_by_username(targetUsername: str):
    """
    Get public data from an Instagram profile
    ---
    tags: [Profile]
    parameters:
      - name: targetUsername
        in: path
        required: true
        schema: { type: string }
      - in: query
        name: username
        required: true
        schema: { type: string }
    responses:
      200: { description: Profile data returned successfully }
    """
    username = request.args.get("username")
    body = GetProfileBody.model_validate({"username": username})
    try:
        client = await resume_session(body.username)
        profile = await client.user_info(targetUsername)
        return jsonify(profile)
    except Exception as exc:
        raise BadRequestError(str(exc))
