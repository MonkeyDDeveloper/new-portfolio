"""
Projects router - CRUD endpoints for projects
"""

from fastapi import APIRouter, HTTPException, Query, status
from schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    MessageResponse
)
from portfolio_controller import PortfolioController
from typing import Optional

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Create a new project")
async def create_project(project: ProjectCreate) -> dict:
    """Create a new project"""
    result = PortfolioController.create_entity(project)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.get("/", response_model=dict, summary="Get all projects")
async def get_projects(
    name: Optional[str] = Query(None, description="Filter by project name"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
) -> dict:
    """Get all projects with optional filters"""
    filters = {"name": name} if name else None

    result = PortfolioController.get_entities(ProjectCreate, filters, skip, limit)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    return result


@router.get("/{project_id}", response_model=dict, summary="Get project by ID")
async def get_project(project_id: int) -> dict:
    """Get a single project by ID"""
    result = PortfolioController.get_entity_by_id(ProjectCreate, project_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    if not result["data"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return result


@router.put("/{project_id}", response_model=dict, summary="Update project")
async def update_project(project_id: int, project: ProjectUpdate) -> dict:
    """Update an existing project"""
    result = PortfolioController.update_entity(project, project_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.delete("/{project_id}", response_model=MessageResponse, summary="Delete project")
async def delete_project(project_id: int) -> MessageResponse:
    """Delete a project by ID"""
    result = PortfolioController.delete_entity(ProjectCreate, project_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return MessageResponse(message=result["message"])
