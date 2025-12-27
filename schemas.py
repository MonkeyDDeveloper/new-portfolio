"""
Pydantic schemas for data validation
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


# ============== Auth Schemas ==============


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class ClientCreate(BaseModel):
    client_id: str = Field(..., min_length=5, max_length=100)
    client_secret: str = Field(..., min_length=10, max_length=100)
    name: str = Field(..., min_length=2, max_length=100)


class ClientResponse(BaseModel):
    id: int
    client_id: str
    name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============== Project Schemas ==============

class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(default="active", max_length=50)
    tags: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = Field(None, max_length=50)
    tags: Optional[str] = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProjectQuery(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    tags: Optional[str] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


# ============== Blog Schemas ==============

class BlogBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    author: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = None
    published: bool = False


class BlogCreate(BlogBase):
    pass


class BlogUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = Field(None, max_length=100)
    tags: Optional[str] = None
    published: Optional[bool] = None


class BlogResponse(BlogBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BlogQuery(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    tags: Optional[str] = None
    published: Optional[bool] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


# ============== Generic Responses ==============

class PaginatedResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List


class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None
