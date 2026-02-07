from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.auth.jwt import decode_access_token
from app.db.session import SessionLocal
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# In backend/app/auth/dependencies.py
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        print(f"AUTH DEBUG: Received token: {token}")
        user_id = decode_access_token(token)
        if not user_id:
            print("AUTH ERROR: Token decoding failed or sub claim missing")
            raise HTTPException(status_code=401, detail="Invalid token")
        
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                print(f"AUTH ERROR: User ID {user_id} not found in database")
                raise HTTPException(status_code=401, detail="User not found")
            return user
    except Exception as e:
        print(f"AUTH ERROR: {str(e)}")
        raise HTTPException(status_code=401, detail="Authentication failed")