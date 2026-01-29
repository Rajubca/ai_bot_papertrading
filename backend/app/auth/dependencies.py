from app.auth.jwt import decode_token


def get_current_user(user=decode_token):
    return user
