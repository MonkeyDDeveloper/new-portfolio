"""
Responsibilities router - CRUD endpoints for responsibilities
"""

from fastapi import APIRouter, HTTPException, Query, status
from schemas import (
    ResponsibilityCreate,
    ResponsibilityUpdate,
    ResponsibilityResponse,
    MessageResponse
)
from portfolio_controller import PortfolioController
from typing import Optional

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Create a new responsibility")
async def create_responsibility(responsibility: ResponsibilityCreate) -> dict:
    """Create a new responsibility"""
    result = PortfolioController.create_entity(responsibility)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.get("/", response_model=dict, summary="Get all responsibilities")
async def get_responsibilities(
    experience_id: Optional[int] = Query(None, description="Filter by experience ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
) -> dict:
    """Get all responsibilities with optional filters"""
    filters = {"experience_id": experience_id} if experience_id is not None else None

    result = PortfolioController.get_entities(ResponsibilityCreate, filters, skip, limit)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    return result


@router.get("/{responsibility_id}", response_model=dict, summary="Get responsibility by ID")
async def get_responsibility(responsibility_id: int) -> dict:
    """Get a single responsibility by ID"""
    result = PortfolioController.get_entity_by_id(ResponsibilityCreate, responsibility_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    if not result["data"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Responsibility not found")
    return result


@router.put("/{responsibility_id}", response_model=dict, summary="Update responsibility")
async def update_responsibility(responsibility_id: int, responsibility: ResponsibilityUpdate) -> dict:
    """Update an existing responsibility"""
    result = PortfolioController.update_entity(responsibility, responsibility_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.delete("/{responsibility_id}", response_model=MessageResponse, summary="Delete responsibility")
async def delete_responsibility(responsibility_id: int) -> MessageResponse:
    """Delete a responsibility by ID"""
    result = PortfolioController.delete_entity(ResponsibilityCreate, responsibility_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return MessageResponse(message=result["message"])
