"""
Portfolio Controller - Generic CRUD operations for all portfolio entities
"""

from pydantic import BaseModel
from database.client import MySQLService
from database.entities.base_entity import BaseEntity
from typing import Optional, Dict, Any


class PortfolioController(BaseModel):
    """Generic controller for portfolio entities following the auth pattern"""

    @staticmethod
    def create_entity(entity: BaseEntity) -> dict:
        """Create a new entity"""
        service = MySQLService()
        return service.create_entity(entity)

    @staticmethod
    def get_entities(entity_class: type[BaseEntity], filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 10) -> dict:
        """Get all entities with optional filters"""
        service = MySQLService()
        return service.find_entities(entity_class, filters, skip, limit)

    @staticmethod
    def get_entity_by_id(entity_class: type[BaseEntity], entity_id: int) -> dict:
        """Get a single entity by ID"""
        service = MySQLService()
        return service.find_entity_by_id(entity_class, entity_id)

    @staticmethod
    def update_entity(entity: BaseEntity, entity_id: int) -> dict:
        """Update an existing entity"""
        service = MySQLService()
        return service.update_entity(entity, entity_id)

    @staticmethod
    def delete_entity(entity_class: type[BaseEntity], entity_id: int) -> dict:
        """Delete an entity by ID"""
        service = MySQLService()
        return service.delete_entity(entity_class, entity_id)
