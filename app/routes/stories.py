
from flask import Blueprint, request, jsonify
from pydantic import BaseModel
from ..errors import BadRequestError
from ..middleware import admin_auth_required
from ..services.instagram_client import resume_session

bp = Blueprint("stories", __name__)

class StoriesBody(BaseModel):
    username: str
    targetUsername: str

@bp.get("/")
@admin_auth_required
async def get_user_stories():
    """
    List user stories
    ---
    tags: [Stories]
    summary: Get user stories
    description: Retrieves stories from a specific user
    security:
      - bearerAuth: []
    produces:
      - application/json
    parameters:
      - in: query
        name: username
        required: true
        schema: { type: string }
        description: Username of the account that will fetch the stories
        example: "my_account"
      - in: query
        name: targetUsername
        required: true
        schema: { type: string }
        description: Username of the target account to get stories from
        example: "target_user"
    responses:
      200:
        description: Stories retrieved successfully
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
                example: "12345678901234567"
              media_type:
                type: string
                example: "PHOTO"
              media_url:
                type: string
                example: "https://example.com/story.jpg"
              taken_at:
                type: string
                example: "2025-08-10T18:00:00Z"
      400:
        description: Error retrieving stories
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error retrieving stories: User not found"
      401:
        description: Missing or invalid authentication token
      403:
        description: Invalid token
    """
    body = StoriesBody.model_validate({
        "username": request.args.get("username"),
        "targetUsername": request.args.get("targetUsername"),
    })
    try:
        client = await resume_session(body.username)
        items = await client.user_stories(body.targetUsername)
        return jsonify(items)
    except Exception as exc:
        raise BadRequestError(str(exc))
