"""
Base entity class for database operations
All database entities should inherit from this class and implement their own query generation
"""

from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Tuple, Dict, Any, Optional


class BaseEntity(BaseModel, ABC):
    """Base class for all database entities - DB agnostic"""

    @classmethod
    @abstractmethod
    def get_table_name(cls) -> str:
        """Return the table name for this entity"""
        pass

    @abstractmethod
    def get_insert_query(self) -> Tuple[str, tuple]:
        """
        Generate INSERT query and params for this entity
        Returns: (query_string, params_tuple)
        """
        pass

    @abstractmethod
    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        """
        Generate UPDATE query and params for this entity
        Returns: (query_string, params_tuple)
        """
        pass

    @classmethod
    @abstractmethod
    def get_select_query(cls, filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 10) -> Tuple[str, tuple]:
        """
        Generate SELECT query with optional filters
        Returns: (query_string, params_tuple)
        """
        pass

    @classmethod
    @abstractmethod
    def get_select_by_id_query(cls, entity_id: int) -> Tuple[str, tuple]:
        """
        Generate SELECT query for a single entity by ID
        Returns: (query_string, params_tuple)
        """
        pass

    @classmethod
    @abstractmethod
    def get_delete_query(cls, entity_id: int) -> Tuple[str, tuple]:
        """
        Generate DELETE query for an entity by ID
        Returns: (query_string, params_tuple)
        """
        pass

    @classmethod
    @abstractmethod
    def get_count_query(cls, filters: Optional[Dict[str, Any]] = None) -> Tuple[str, tuple]:
        """
        Generate COUNT query with optional filters
        Returns: (query_string, params_tuple)
        """
        pass