from fastapi import Header, HTTPException


def decode_token(authorization: str = Header(None)):
    """
    Temporary local-dev auth.
    Always returns a mock user.
    """

    # In production, validate JWT here
    if authorization is None:
        # For now allow access even without token
        return {"id": 1}

    return {"id": 1}
