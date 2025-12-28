from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, List
import pymysql
import pymysql.cursors
from database.entities.api_db_entities import FindUserResponse, ApiUser, UserInDB, AuthResponse
from database.entities.base_entity import BaseEntity
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

    @abstractmethod
    def create_entity(self, entity: BaseEntity) -> dict:
        """Create a new entity in the database"""
        pass

    @abstractmethod
    def find_entities(self, entity_class: type[BaseEntity], filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 10) -> dict:
        """Find entities with optional filters and pagination"""
        pass

    @abstractmethod
    def find_entity_by_id(self, entity_class: type[BaseEntity], entity_id: int) -> dict:
        """Find a single entity by ID"""
        pass

    @abstractmethod
    def update_entity(self, entity: BaseEntity, entity_id: int) -> dict:
        """Update an existing entity"""
        pass

    @abstractmethod
    def delete_entity(self, entity_class: type[BaseEntity], entity_id: int) -> dict:
        """Delete an entity by ID"""
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
                    username=result.get('username'),
                    password=result.get('password')
                )
                return FindUserResponse(success=True, user=user_in_db, message="User found")
        except Exception as e:
            return FindUserResponse(success=False, user=None, message=f"There was an error querying the database, looking for user {api_user.username}: {str(e)}")

    # ============== Generic Entity CRUD Methods ==============

    def create_entity(self, entity: BaseEntity) -> dict:
        """Create a new entity using its get_insert_query method"""
        try:
            with self._connection.cursor() as cursor:
                query, params = entity.get_insert_query()
                cursor.execute(query, params)
                self._connection.commit()
                return {"success": True, "id": cursor.lastrowid, "message": "Entity created successfully"}
        except Exception as e:
            self._connection.rollback()
            return {"success": False, "message": f"Error creating entity: {str(e)}"}

    def find_entities(self, entity_class: type[BaseEntity], filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 10) -> dict:
        """Find entities using the entity class's get_select_query method"""
        try:
            with self._connection.cursor() as cursor:
                # Get query from entity class
                query, params = entity_class.get_select_query(filters=filters, skip=skip, limit=limit)
                cursor.execute(query, params)
                results = cursor.fetchall()

                # Get count
                count_query, count_params = entity_class.get_count_query(filters=filters)
                cursor.execute(count_query, count_params)
                total = cursor.fetchone()['total']

                return {"success": True, "data": results, "total": total}
        except Exception as e:
            return {"success": False, "message": f"Error fetching entities: {str(e)}"}

    def find_entity_by_id(self, entity_class: type[BaseEntity], entity_id: int) -> dict:
        """Find a single entity by ID using the entity class's get_select_by_id_query method"""
        try:
            with self._connection.cursor() as cursor:
                query, params = entity_class.get_select_by_id_query(entity_id)
                cursor.execute(query, params)
                result = cursor.fetchone()
                return {"success": True, "data": result}
        except Exception as e:
            return {"success": False, "message": f"Error fetching entity: {str(e)}"}

    def update_entity(self, entity: BaseEntity, entity_id: int) -> dict:
        """Update an entity using its get_update_query method"""
        try:
            with self._connection.cursor() as cursor:
                query, params = entity.get_update_query(entity_id)
                cursor.execute(query, params)
                self._connection.commit()
                return {"success": True, "message": "Entity updated successfully"}
        except ValueError as ve:
            return {"success": False, "message": str(ve)}
        except Exception as e:
            self._connection.rollback()
            return {"success": False, "message": f"Error updating entity: {str(e)}"}

    def delete_entity(self, entity_class: type[BaseEntity], entity_id: int) -> dict:
        """Delete an entity using the entity class's get_delete_query method"""
        try:
            with self._connection.cursor() as cursor:
                query, params = entity_class.get_delete_query(entity_id)
                cursor.execute(query, params)
                self._connection.commit()
                return {"success": True, "message": "Entity deleted successfully"}
        except Exception as e:
            self._connection.rollback()
            return {"success": False, "message": f"Error deleting entity: {str(e)}"}


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

    # ============== Generic Entity CRUD Methods ==============

    def create_entity(self, entity: BaseEntity) -> dict:
        """Create a new entity"""
        with self.create_connection(self.config) as connection:
            return connection.create_entity(entity)

    def find_entities(self, entity_class: type[BaseEntity], filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 10) -> dict:
        """Find entities with optional filters"""
        with self.create_connection(self.config) as connection:
            return connection.find_entities(entity_class, filters, skip, limit)

    def find_entity_by_id(self, entity_class: type[BaseEntity], entity_id: int) -> dict:
        """Find a single entity by ID"""
        with self.create_connection(self.config) as connection:
            return connection.find_entity_by_id(entity_class, entity_id)

    def update_entity(self, entity: BaseEntity, entity_id: int) -> dict:
        """Update an existing entity"""
        with self.create_connection(self.config) as connection:
            return connection.update_entity(entity, entity_id)

    def delete_entity(self, entity_class: type[BaseEntity], entity_id: int) -> dict:
        """Delete an entity by ID"""
        with self.create_connection(self.config) as connection:
            return connection.delete_entity(entity_class, entity_id)

    def __init__(self):
        self.load_config()
