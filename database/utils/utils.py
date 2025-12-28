from decouple import config
import jwt
from database.entities.api_db_entities import ApiUser

def generate_token_for_api_user(api_user: ApiUser) -> str:
    """Generate token for API entities"""
    token = jwt.encode(api_user.model_dump(), config('SECRET_KEY'), algorithm="HS256")
    return token


def verify_token(token: str | None) -> bool:
    """Verify token"""
    if not token:
        return False

    try:
        if token.startswith("Bearer "):
            token = token[7:]

        jwt.decode(token, config('SECRET_KEY'), algorithms=["HS256"])
        return True
    except Exception as e:
        return False
