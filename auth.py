"""
Authentication system with JWT and IP whitelist
"""

from pydantic import BaseModel
from database.client import MySQLService
from database.entities.api_db_entities import TokenRequest, AuthResponse

class AuthController(BaseModel):

    @staticmethod
    def authenticate_client(token_request: TokenRequest) -> AuthResponse:
        """Authenticate client with credentials"""
        service = MySQLService() # by default we are using mysql service
        return service.auth_user(token_request.api_user)
