from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.db.session import SessionLocal
from app.analytics.engine import get_trade_stats

router = APIRouter()

@router.get("")
def analytics(user=Depends(get_current_user)):
    db = SessionLocal()
    stats = get_trade_stats(db, user["id"])
    db.close()
    return stats
