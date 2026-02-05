from fastapi import APIRouter, Depends
from app.auth.dependencies import decode_access_token
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("")
def analytics(
    user=Depends(decode_access_token),
    db=Depends(get_db)
):
    # user["id"] is now REAL
    return {
        "total_trades": 0,
        "win_rate": 0,
        "avg_win": 0,
        "expectancy": 0,
        "max_win_streak": 0
    }
