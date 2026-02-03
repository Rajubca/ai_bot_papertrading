from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.auth.dependencies import get_current_user
from app.api.pnl import get_today_pnl

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("")
def analytics(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return get_today_pnl(db=db, user=user)
