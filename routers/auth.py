"""
Authentication router
"""

from fastapi import APIRouter
from database.entities.api_db_entities import AuthResponse, TokenRequest
from auth import AuthController

router = APIRouter()


@router.post("/token", response_model=AuthResponse, summary="Get access token")
async def get_token(credentials: TokenRequest) -> AuthResponse:
    """
    Get an access token using username and password.
    """
    auth_response: AuthResponse = AuthController.authenticate_client(token_request=credentials)
    
    return auth_response