from fastapi import APIRouter, Depends, HTTPException
from groq import Groq
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.config import settings
from app.auth.dependencies import decode_access_token as decode_token
from app.db.session import SessionLocal
from app.db.models import AgentChatHistory, Trade
from app.analytics.stats import get_trade_stats  # your existing stats logic

router = APIRouter()

# ---------------- DB ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- GROQ ----------------
groq_client = Groq(api_key=settings.GROQ_API_KEY)

SYSTEM_PROMPT = """
You are an AI trading performance analyst.
You analyze user trades, risk behavior, and performance.
Be concise, practical, and trading-focused.
Do NOT give financial advice.
"""

# ---------------- SCHEMA ----------------
class ChatRequest(BaseModel):
    message: str

# ---------------- CHAT ----------------
@router.post("/chat")
def chat_with_agent(
    payload: ChatRequest,
    user=Depends(decode_token),
    db: Session = Depends(get_db),
):
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="Empty message")

    user_id = user["id"]

    # ---- Fetch trading stats ----
    stats = get_trade_stats(db=db, user_id=user_id)

    context = f"""
User Trading Stats:
- Total Trades: {stats['total_trades']}
- Win Rate: {stats['win_rate']}%
- Avg Win: {stats['avg_win']}
- Avg Loss: {stats['avg_loss']}
- Expectancy: {stats['expectancy']}
- Max Win Streak: {stats['max_win_streak']}
- Max Loss Streak: {stats['max_loss_streak']}
"""

    # ---- Save user message ----
    db.add(
        AgentChatHistory(
            user_id=user_id,
            role="USER",
            message=payload.message,
        )
    )
    db.commit()

    # ---- Call Groq ----
    try:
        completion = groq_client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "system", "content": context},
                {"role": "user", "content": payload.message},
            ],
            temperature=0.3,
            max_tokens=300,
        )

        ai_reply = completion.choices[0].message.content.strip()

    except Exception as e:
        ai_reply = "AI service temporarily unavailable."

    # ---- Save AI response ----
    db.add(
        AgentChatHistory(
            user_id=user_id,
            role="AGENT",
            message=ai_reply,
        )
    )
    db.commit()

    return {
        "role": "AGENT",
        "reply": ai_reply,
    }
