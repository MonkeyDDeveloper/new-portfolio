"""
MySQL-specific implementation of BaseEntity
All MySQL entities should inherit from this class
"""

from database.entities.base_entity import BaseEntity
from typing import Tuple, Dict, Any, Optional
from abc import abstractmethod


class MySQLEntity(BaseEntity):
    """Base class for MySQL entities with SQL query generation"""

    @classmethod
    @abstractmethod
    def get_table_name(cls) -> str:
        """Return the table name for this entity"""
        pass

    @classmethod
    @abstractmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        """
        Return mapping of Python field names to database column names
        Example: {"name": "name", "logo_path": "logo_path"}
        """
        pass

    @abstractmethod
    def get_insert_query(self) -> Tuple[str, tuple]:
        """
        Generate INSERT query and params for this entity
        Must be implemented by each entity to specify which fields to insert
        """
        pass

    @abstractmethod
    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        """
        Generate UPDATE query and params for this entity
        Must be implemented by each entity to specify which fields to update
        """
        pass

    @classmethod
    def get_select_query(cls, filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 10) -> Tuple[str, tuple]:
        """Generate SELECT query with optional filters"""
        table_name = cls.get_table_name()
        query = f"SELECT * FROM {table_name}"
        params = []

        if filters:
            where_clauses = []
            for key, value in filters.items():
                if value is not None:
                    if isinstance(value, str):
                        where_clauses.append(f"{key} LIKE %s")
                        params.append(f"%{value}%")
                    else:
                        where_clauses.append(f"{key} = %s")
                        params.append(value)

            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

        query += " LIMIT %s OFFSET %s"
        params.extend([limit, skip])

        return (query, tuple(params))

    @classmethod
    def get_select_by_id_query(cls, entity_id: int) -> Tuple[str, tuple]:
        """Generate SELECT query for a single entity by ID"""
        table_name = cls.get_table_name()
        query = f"SELECT * FROM {table_name} WHERE id = %s"
        return (query, (entity_id,))

    @classmethod
    def get_delete_query(cls, entity_id: int) -> Tuple[str, tuple]:
        """Generate DELETE query for an entity by ID"""
        table_name = cls.get_table_name()
        query = f"DELETE FROM {table_name} WHERE id = %s"
        return (query, (entity_id,))

    @classmethod
    def get_count_query(cls, filters: Optional[Dict[str, Any]] = None) -> Tuple[str, tuple]:
        """Generate COUNT query with optional filters"""
        table_name = cls.get_table_name()
        query = f"SELECT COUNT(*) as total FROM {table_name}"
        params = []

        if filters:
            where_clauses = []
            for key, value in filters.items():
                if value is not None:
                    if isinstance(value, str):
                        where_clauses.append(f"{key} LIKE %s")
                        params.append(f"%{value}%")
                    else:
                        where_clauses.append(f"{key} = %s")
                        params.append(value)

            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)

        return (query, tuple(params))