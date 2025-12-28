"""
Company Experiences router - CRUD endpoints for company-experience relationships
"""

from fastapi import APIRouter, HTTPException, Query, status
from schemas import (
    CompanyExperienceCreate,
    CompanyExperienceResponse,
    MessageResponse
)
from portfolio_controller import PortfolioController
from typing import Optional

router = APIRouter()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Create a new company-experience relationship")
async def create_company_experience(company_experience: CompanyExperienceCreate) -> dict:
    """Create a new company-experience relationship"""
    result = PortfolioController.create_entity(company_experience)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.get("/", response_model=dict, summary="Get all company-experience relationships")
async def get_company_experiences(
    company_id: Optional[int] = Query(None, description="Filter by company ID"),
    experience_id: Optional[int] = Query(None, description="Filter by experience ID"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
) -> dict:
    """Get all company-experience relationships with optional filters"""
    filters = {}
    if company_id is not None:
        filters["company_id"] = company_id
    if experience_id is not None:
        filters["experience_id"] = experience_id

    result = PortfolioController.get_entities(CompanyExperienceCreate, filters if filters else None, skip, limit)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    return result


@router.get("/{company_experience_id}", response_model=dict, summary="Get company-experience relationship by ID")
async def get_company_experience(company_experience_id: int) -> dict:
    """Get a single company-experience relationship by ID"""
    result = PortfolioController.get_entity_by_id(CompanyExperienceCreate, company_experience_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    if not result["data"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company-experience relationship not found")
    return result


@router.delete("/{company_experience_id}", response_model=MessageResponse, summary="Delete company-experience relationship")
async def delete_company_experience(company_experience_id: int) -> MessageResponse:
    """Delete a company-experience relationship by ID"""
    result = PortfolioController.delete_entity(CompanyExperienceCreate, company_experience_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return MessageResponse(message=result["message"])
