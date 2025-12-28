"""
Professional Experiences router - CRUD endpoints for professional experiences
"""

from fastapi import APIRouter, HTTPException, Query, status
from schemas import (
    ProfessionalExperienceCreate,
    ProfessionalExperienceUpdate,
    ProfessionalExperienceResponse,
    MessageResponse
)
from portfolio_controller import PortfolioController
from typing import Optional

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Create a new professional experience")
async def create_experience(experience: ProfessionalExperienceCreate) -> dict:
    """Create a new professional experience"""
    result = PortfolioController.create_entity(experience)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.get("/", response_model=dict, summary="Get all professional experiences")
async def get_experiences(
    title: Optional[str] = Query(None, description="Filter by experience title"),
    is_current: Optional[bool] = Query(None, description="Filter by current employment status"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
) -> dict:
    """Get all professional experiences with optional filters"""
    filters = {}
    if title:
        filters["title"] = title
    if is_current is not None:
        filters["is_current"] = is_current

    result = PortfolioController.get_entities(ProfessionalExperienceCreate, filters if filters else None, skip, limit)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    return result


@router.get("/{experience_id}", response_model=dict, summary="Get professional experience by ID")
async def get_experience(experience_id: int) -> dict:
    """Get a single professional experience by ID"""
    result = PortfolioController.get_entity_by_id(ProfessionalExperienceCreate, experience_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    if not result["data"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Professional experience not found")
    return result


@router.put("/{experience_id}", response_model=dict, summary="Update professional experience")
async def update_experience(experience_id: int, experience: ProfessionalExperienceUpdate) -> dict:
    """Update an existing professional experience"""
    result = PortfolioController.update_entity(experience, experience_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.delete("/{experience_id}", response_model=MessageResponse, summary="Delete professional experience")
async def delete_experience(experience_id: int) -> MessageResponse:
    """Delete a professional experience by ID"""
    result = PortfolioController.delete_entity(ProfessionalExperienceCreate, experience_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return MessageResponse(message=result["message"])
