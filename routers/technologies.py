"""
Technologies router - CRUD endpoints for technologies
"""

from fastapi import APIRouter, HTTPException, Query, status
from schemas import (
    TechnologyCreate,
    TechnologyUpdate,
    TechnologyResponse,
    MessageResponse
)
from portfolio_controller import PortfolioController
from typing import Optional

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Create a new technology")
async def create_technology(technology: TechnologyCreate) -> dict:
    """Create a new technology"""
    result = PortfolioController.create_entity(technology)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.get("/", response_model=dict, summary="Get all technologies")
async def get_technologies(
    name: Optional[str] = Query(None, description="Filter by technology name"),
    abbr: Optional[str] = Query(None, description="Filter by technology abbreviation"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
) -> dict:
    """Get all technologies with optional filters"""
    filters = {}
    if name:
        filters["name"] = name
    if abbr:
        filters["abbr"] = abbr

    result = PortfolioController.get_entities(TechnologyCreate, filters if filters else None, skip, limit)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    return result


@router.get("/{technology_id}", response_model=dict, summary="Get technology by ID")
async def get_technology(technology_id: int) -> dict:
    """Get a single technology by ID"""
    result = PortfolioController.get_entity_by_id(TechnologyCreate, technology_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    if not result["data"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Technology not found")
    return result


@router.put("/{technology_id}", response_model=dict, summary="Update technology")
async def update_technology(technology_id: int, technology: TechnologyUpdate) -> dict:
    """Update an existing technology"""
    result = PortfolioController.update_entity(technology, technology_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.delete("/{technology_id}", response_model=MessageResponse, summary="Delete technology")
async def delete_technology(technology_id: int) -> MessageResponse:
    """Delete a technology by ID"""
    result = PortfolioController.delete_entity(TechnologyCreate, technology_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return MessageResponse(message=result["message"])
