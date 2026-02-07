from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config import settings

def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.JWT_EXPIRE_MINUTES
        )
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )
    return token



from jose import jwt, JWTError
from app.config import settings


def decode_access_token(token: str):
    """
    Decodes JWT token and returns user_id
    """

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )

        sub = payload.get("sub")

        if sub is None:
            return None

        return int(sub)

    except JWTError as e:
        print("JWT Decode Error:", e)
        return None

    except Exception as e:
        print("Token Error:", e)
        return None
