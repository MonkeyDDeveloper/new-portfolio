"""
Companies router - CRUD endpoints for companies
"""

from fastapi import APIRouter, HTTPException, status, Query
from schemas import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse,
    MessageResponse
)
from portfolio_controller import PortfolioController
from typing import Optional

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Create a new company")
async def create_company(company: CompanyCreate) -> dict:
    """Create a new company"""
    result = PortfolioController.create_entity(company)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.get("/", response_model=dict, summary="Get all companies")
async def get_companies(
    name: Optional[str] = Query(None, description="Filter by company name"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max number of records to return")
) -> dict:
    """Get all companies with optional filters"""
    filters = {"name": name} if name else None

    result = PortfolioController.get_entities(CompanyCreate, filters, skip, limit)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    return result


@router.get("/{company_id}", response_model=dict, summary="Get company by ID")
async def get_company(company_id: int) -> dict:
    """Get a single company by ID"""
    result = PortfolioController.get_entity_by_id(CompanyCreate, company_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result["message"])
    if not result["data"]:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return result


@router.put("/{company_id}", response_model=dict, summary="Update company")
async def update_company(company_id: int, company: CompanyUpdate) -> dict:
    """Update an existing company"""
    result = PortfolioController.update_entity(company, company_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return result


@router.delete("/{company_id}", response_model=MessageResponse, summary="Delete company")
async def delete_company(company_id: int) -> MessageResponse:
    """Delete a company by ID"""
    result = PortfolioController.delete_entity(CompanyCreate, company_id)
    if not result["success"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=result["message"])
    return MessageResponse(message=result["message"])
