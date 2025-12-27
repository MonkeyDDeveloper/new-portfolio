from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Any
import pymysql
import pymysql.cursors
from database.entities.api_db_entities import FindUserResponse, ApiUser, UserInDB, AuthResponse
from decouple import config
from database.utils.password import verify_password
from database.utils.utils import generate_token_for_api_user


# Connections

class Connection(ABC, BaseModel):
    config: dict

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def find_user(self, user: ApiUser) -> FindUserResponse:
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()


class MySQLConnection(Connection):
    _connection: Any = None

    def connect(self):
        self._connection = pymysql.connect(
            host=self.config.get('HOST'),
            port=int(self.config.get('DB_PORT')),
            user=self.config.get('USERNAME'),
            password=self.config.get('PASSWORD'),
            database=self.config.get('DATABASE'),
            cursorclass=pymysql.cursors.DictCursor
        )

    def disconnect(self):
        if self._connection:
            self._connection.close()

    def find_user(self, api_user: ApiUser) -> FindUserResponse:
        try:
            with self._connection.cursor() as cursor:
                query = "SELECT * FROM users WHERE username = %s"
                cursor.execute(query, (api_user.username,))
                result = cursor.fetchone()
                if result is None:
                    return FindUserResponse(success=True, user=None, message="No user found")
                user_in_db = UserInDB(
                    username=result.get('USERNAME'),
                    password=result.get('PASSWORD')
                )
                return FindUserResponse(success=True, user=user_in_db, message="User found")
        except Exception as e:
            return FindUserResponse(success=False, user=None, message=f"There was an error querying the database, looking for user {api_user.username}: {str(e)}")


# Services

class DBService(ABC):
    config: dict

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def load_config(self):
        pass

    @abstractmethod
    def create_connection(self, config: dict):
        pass

    @abstractmethod
    def auth_user(self, api_user: ApiUser):
        pass


class MySQLService(DBService):

    def load_config(self):
        self.config = {
            "HOST": config("HOST"),
            "DB_PORT": config("DB_PORT"),
            "USERNAME": config("USERNAME"),
            "PASSWORD": config("PASSWORD"),
            "DATABASE": config("DATABASE"),
        }

    def create_connection(self, config: dict):
        return MySQLConnection(config=config)

    def auth_user(self, api_user: ApiUser) -> AuthResponse:
        with self.create_connection(self.config) as connection:
            find_user_response: FindUserResponse = connection.find_user(
                api_user=api_user
            )
            if not isinstance(find_user_response.user, UserInDB):
                return AuthResponse(
                    success=False,
                    message=find_user_response.message,
                    token=None
                )

            is_valid_password = verify_password(api_user.password, find_user_response.user.password)

            if not is_valid_password:
                return AuthResponse(
                    success=False,
                    message=f"The password provided is not correct",
                    token=None
                )

            token = generate_token_for_api_user(api_user=api_user)

            return AuthResponse(
                success=True,
                message="User authenticated successfully",
                token=token
            )

    def __init__(self):
        self.load_config()
