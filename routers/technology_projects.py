"""
Technology Projects router - CRUD endpoints for technology-project relationships
"""

from fastapi import APIRouter, HTTPException, Query, status
from schemas import (
    TechnologyProjectCreate,
    TechnologyProjectResponse,
    MessageResponse
)
from portfolio_controller import PortfolioController
from typing import Optional

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Create a new technology-project relationship")
async def create_technology_project(technology_project: TechnologyProjectCreate) -> dict:
    """Create a new technology-project relationship"""
    result = PortfolioController.create_entity(technology_project)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.get("/", response_model=dict, summary="Get all technology-project relationships")
async def get_technology_projects(
    technology_id: Optional[int] = Query(None, description="Filter by technology ID"),
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
) -> dict:
    """Get all technology-project relationships with optional filters"""
    filters = {}
    if technology_id is not None:
        filters["technology_id"] = technology_id
    if project_id is not None:
        filters["project_id"] = project_id

    result = PortfolioController.get_entities(TechnologyProjectCreate, filters if filters else None, skip, limit)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    return result


@router.get("/{technology_project_id}", response_model=dict, summary="Get technology-project relationship by ID")
async def get_technology_project(technology_project_id: int) -> dict:
    """Get a single technology-project relationship by ID"""
    result = PortfolioController.get_entity_by_id(TechnologyProjectCreate, technology_project_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    if not result["data"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Technology-project relationship not found")
    return result


@router.delete("/{technology_project_id}", response_model=MessageResponse, summary="Delete technology-project relationship")
async def delete_technology_project(technology_project_id: int) -> MessageResponse:
    """Delete a technology-project relationship by ID"""
    result = PortfolioController.delete_entity(TechnologyProjectCreate, technology_project_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return MessageResponse(message=result["message"])
