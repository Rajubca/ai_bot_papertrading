from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.agent.chat import chat_with_agent
from app.db import crud

router = APIRouter()

@router.post("/chat")
def chat(payload: dict, user=Depends(get_current_user)):
    context = crud.build_user_context(user["id"])
    return chat_with_agent(payload["message"], context)
