from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.auth.dependencies import get_current_user

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
def chat_with_agent(
    payload: ChatRequest,
    user=Depends(get_current_user),
):
    return {
        "role": "AGENT",
        "reply": f"AI analysis placeholder for user {user['id']}: {payload.message}",
    }
