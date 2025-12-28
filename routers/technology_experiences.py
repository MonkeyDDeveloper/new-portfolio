"""
Technology Experiences router - CRUD endpoints for technology-experience relationships
"""

from fastapi import APIRouter, HTTPException, Query, status
from schemas import (
    TechnologyExperienceCreate,
    TechnologyExperienceResponse,
    MessageResponse
)
from portfolio_controller import PortfolioController
from typing import Optional

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Create a new technology-experience relationship")
async def create_technology_experience(technology_experience: TechnologyExperienceCreate) -> dict:
    """Create a new technology-experience relationship"""
    result = PortfolioController.create_entity(technology_experience)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.get("/", response_model=dict, summary="Get all technology-experience relationships")
async def get_technology_experiences(
    technology_id: Optional[int] = Query(None, description="Filter by technology ID"),
    experience_id: Optional[int] = Query(None, description="Filter by experience ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
) -> dict:
    """Get all technology-experience relationships with optional filters"""
    filters = {}
    if technology_id is not None:
        filters["technology_id"] = technology_id
    if experience_id is not None:
        filters["experience_id"] = experience_id

    result = PortfolioController.get_entities(TechnologyExperienceCreate, filters if filters else None, skip, limit)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    return result


@router.get("/{technology_experience_id}", response_model=dict, summary="Get technology-experience relationship by ID")
async def get_technology_experience(technology_experience_id: int) -> dict:
    """Get a single technology-experience relationship by ID"""
    result = PortfolioController.get_entity_by_id(TechnologyExperienceCreate, technology_experience_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    if not result["data"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Technology-experience relationship not found")
    return result


@router.delete("/{technology_experience_id}", response_model=MessageResponse, summary="Delete technology-experience relationship")
async def delete_technology_experience(technology_experience_id: int) -> MessageResponse:
    """Delete a technology-experience relationship by ID"""
    result = PortfolioController.delete_entity(TechnologyExperienceCreate, technology_experience_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return MessageResponse(message=result["message"])
