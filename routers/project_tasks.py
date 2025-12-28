"""
Project Tasks router - CRUD endpoints for project tasks
"""

from fastapi import APIRouter, HTTPException, Query, status
from schemas import (
    ProjectTaskCreate,
    ProjectTaskUpdate,
    ProjectTaskResponse,
    MessageResponse
)
from portfolio_controller import PortfolioController
from typing import Optional

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Create a new project task")
async def create_project_task(project_task: ProjectTaskCreate) -> dict:
    """Create a new project task"""
    result = PortfolioController.create_entity(project_task)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.get("/", response_model=dict, summary="Get all project tasks")
async def get_project_tasks(
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    name: Optional[str] = Query(None, description="Filter by task name"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
) -> dict:
    """Get all project tasks with optional filters"""
    filters = {}
    if project_id is not None:
        filters["project_id"] = project_id
    if name:
        filters["name"] = name

    result = PortfolioController.get_entities(ProjectTaskCreate, filters if filters else None, skip, limit)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    return result


@router.get("/{task_id}", response_model=dict, summary="Get project task by ID")
async def get_project_task(task_id: int) -> dict:
    """Get a single project task by ID"""
    result = PortfolioController.get_entity_by_id(ProjectTaskCreate, task_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    if not result["data"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project task not found")
    return result


@router.put("/{task_id}", response_model=dict, summary="Update project task")
async def update_project_task(task_id: int, project_task: ProjectTaskUpdate) -> dict:
    """Update an existing project task"""
    result = PortfolioController.update_entity(project_task, task_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.delete("/{task_id}", response_model=MessageResponse, summary="Delete project task")
async def delete_project_task(task_id: int) -> MessageResponse:
    """Delete a project task by ID"""
    result = PortfolioController.delete_entity(ProjectTaskCreate, task_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return MessageResponse(message=result["message"])
