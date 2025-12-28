"""
Pydantic schemas for data validation
"""

from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List, Tuple, Dict, Any
from database.entities.mysql_entity import MySQLEntity


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


# ============== Company Schemas ==============

class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    logo_path: str = Field(..., min_length=1, max_length=500)


class CompanyCreate(MySQLEntity):
    name: str = Field(..., min_length=1, max_length=200)
    logo_path: str = Field(..., min_length=1, max_length=500)

    @classmethod
    def get_table_name(cls) -> str:
        return "companies"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"name": "name", "logo_path": "logo_path"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        query = "INSERT INTO companies (name, logo_path) VALUES (%s, %s)"
        params = (self.name, self.logo_path)
        return (query, params)

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        query = "UPDATE companies SET name = %s, logo_path = %s WHERE id = %s"
        params = (self.name, self.logo_path, entity_id)
        return (query, params)


class CompanyUpdate(MySQLEntity):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    logo_path: Optional[str] = Field(None, min_length=1, max_length=500)

    @classmethod
    def get_table_name(cls) -> str:
        return "companies"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"name": "name", "logo_path": "logo_path"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        raise NotImplementedError("Update schema should not be used for insert operations")

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        updates = []
        params = []

        if self.name is not None:
            updates.append("name = %s")
            params.append(self.name)
        if self.logo_path is not None:
            updates.append("logo_path = %s")
            params.append(self.logo_path)

        if not updates:
            raise ValueError("No fields to update")

        query = f"UPDATE companies SET {', '.join(updates)} WHERE id = %s"
        params.append(entity_id)
        return (query, tuple(params))


class CompanyResponse(CompanyBase):
    id: int

    class Config:
        from_attributes = True


class CompanyQuery(BaseModel):
    name: Optional[str] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


# ============== Technology Schemas ==============

class TechnologyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    abbr: str = Field(..., min_length=1, max_length=20)


class TechnologyCreate(MySQLEntity):
    name: str = Field(..., min_length=1, max_length=100)
    abbr: str = Field(..., min_length=1, max_length=20)

    @classmethod
    def get_table_name(cls) -> str:
        return "technologies"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"name": "name", "abbr": "abbr"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        query = "INSERT INTO technologies (name, abbr) VALUES (%s, %s)"
        params = (self.name, self.abbr)
        return (query, params)

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        query = "UPDATE technologies SET name = %s, abbr = %s WHERE id = %s"
        params = (self.name, self.abbr, entity_id)
        return (query, params)


class TechnologyUpdate(MySQLEntity):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    abbr: Optional[str] = Field(None, min_length=1, max_length=20)

    @classmethod
    def get_table_name(cls) -> str:
        return "technologies"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"name": "name", "abbr": "abbr"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        raise NotImplementedError("Update schema should not be used for insert operations")

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        updates = []
        params = []

        if self.name is not None:
            updates.append("name = %s")
            params.append(self.name)
        if self.abbr is not None:
            updates.append("abbr = %s")
            params.append(self.abbr)

        if not updates:
            raise ValueError("No fields to update")

        query = f"UPDATE technologies SET {', '.join(updates)} WHERE id = %s"
        params.append(entity_id)
        return (query, tuple(params))


class TechnologyResponse(TechnologyBase):
    id: int

    class Config:
        from_attributes = True


class TechnologyQuery(BaseModel):
    name: Optional[str] = None
    abbr: Optional[str] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


# ============== Professional Experience Schemas ==============

class ProfessionalExperienceBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    start_date: date
    end_date: date
    is_current: bool = False


class ProfessionalExperienceCreate(MySQLEntity):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    start_date: date
    end_date: date
    is_current: bool = False

    @classmethod
    def get_table_name(cls) -> str:
        return "professional_experiences"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {
            "title": "title",
            "description": "description",
            "start_date": "start_date",
            "end_date": "end_date",
            "is_current": "is_current"
        }

    def get_insert_query(self) -> Tuple[str, tuple]:
        query = "INSERT INTO professional_experiences (title, description, start_date, end_date, is_current) VALUES (%s, %s, %s, %s, %s)"
        params = (self.title, self.description, self.start_date, self.end_date, self.is_current)
        return (query, params)

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        query = "UPDATE professional_experiences SET title = %s, description = %s, start_date = %s, end_date = %s, is_current = %s WHERE id = %s"
        params = (self.title, self.description, self.start_date, self.end_date, self.is_current, entity_id)
        return (query, params)


class ProfessionalExperienceUpdate(MySQLEntity):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None

    @classmethod
    def get_table_name(cls) -> str:
        return "professional_experiences"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {
            "title": "title",
            "description": "description",
            "start_date": "start_date",
            "end_date": "end_date",
            "is_current": "is_current"
        }

    def get_insert_query(self) -> Tuple[str, tuple]:
        raise NotImplementedError("Update schema should not be used for insert operations")

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        updates = []
        params = []

        if self.title is not None:
            updates.append("title = %s")
            params.append(self.title)
        if self.description is not None:
            updates.append("description = %s")
            params.append(self.description)
        if self.start_date is not None:
            updates.append("start_date = %s")
            params.append(self.start_date)
        if self.end_date is not None:
            updates.append("end_date = %s")
            params.append(self.end_date)
        if self.is_current is not None:
            updates.append("is_current = %s")
            params.append(self.is_current)

        if not updates:
            raise ValueError("No fields to update")

        query = f"UPDATE professional_experiences SET {', '.join(updates)} WHERE id = %s"
        params.append(entity_id)
        return (query, tuple(params))


class ProfessionalExperienceResponse(ProfessionalExperienceBase):
    id: int

    class Config:
        from_attributes = True


class ProfessionalExperienceQuery(BaseModel):
    title: Optional[str] = None
    is_current: Optional[bool] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


# ============== Project Schemas ==============

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    github_uri: str = Field(..., min_length=1, max_length=500)


class ProjectCreate(MySQLEntity):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    github_uri: str = Field(..., min_length=1, max_length=500)

    @classmethod
    def get_table_name(cls) -> str:
        return "projects"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"name": "name", "description": "description", "github_uri": "github_uri"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        query = "INSERT INTO projects (name, description, github_uri) VALUES (%s, %s, %s)"
        params = (self.name, self.description, self.github_uri)
        return (query, params)

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        query = "UPDATE projects SET name = %s, description = %s, github_uri = %s WHERE id = %s"
        params = (self.name, self.description, self.github_uri, entity_id)
        return (query, params)


class ProjectUpdate(MySQLEntity):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    github_uri: Optional[str] = Field(None, min_length=1, max_length=500)

    @classmethod
    def get_table_name(cls) -> str:
        return "projects"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"name": "name", "description": "description", "github_uri": "github_uri"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        raise NotImplementedError("Update schema should not be used for insert operations")

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        updates = []
        params = []

        if self.name is not None:
            updates.append("name = %s")
            params.append(self.name)
        if self.description is not None:
            updates.append("description = %s")
            params.append(self.description)
        if self.github_uri is not None:
            updates.append("github_uri = %s")
            params.append(self.github_uri)

        if not updates:
            raise ValueError("No fields to update")

        query = f"UPDATE projects SET {', '.join(updates)} WHERE id = %s"
        params.append(entity_id)
        return (query, tuple(params))


class ProjectResponse(ProjectBase):
    id: int

    class Config:
        from_attributes = True


class ProjectQuery(BaseModel):
    name: Optional[str] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


# ============== Project Task Schemas ==============

class ProjectTaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    project_id: int


class ProjectTaskCreate(MySQLEntity):
    name: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    project_id: int

    @classmethod
    def get_table_name(cls) -> str:
        return "project_tasks"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"name": "name", "description": "description", "project_id": "project_id"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        query = "INSERT INTO project_tasks (name, description, project_id) VALUES (%s, %s, %s)"
        params = (self.name, self.description, self.project_id)
        return (query, params)

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        query = "UPDATE project_tasks SET name = %s, description = %s, project_id = %s WHERE id = %s"
        params = (self.name, self.description, self.project_id, entity_id)
        return (query, params)


class ProjectTaskUpdate(MySQLEntity):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    project_id: Optional[int] = None

    @classmethod
    def get_table_name(cls) -> str:
        return "project_tasks"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"name": "name", "description": "description", "project_id": "project_id"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        raise NotImplementedError("Update schema should not be used for insert operations")

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        updates = []
        params = []

        if self.name is not None:
            updates.append("name = %s")
            params.append(self.name)
        if self.description is not None:
            updates.append("description = %s")
            params.append(self.description)
        if self.project_id is not None:
            updates.append("project_id = %s")
            params.append(self.project_id)

        if not updates:
            raise ValueError("No fields to update")

        query = f"UPDATE project_tasks SET {', '.join(updates)} WHERE id = %s"
        params.append(entity_id)
        return (query, tuple(params))


class ProjectTaskResponse(ProjectTaskBase):
    id: int

    class Config:
        from_attributes = True


class ProjectTaskQuery(BaseModel):
    project_id: Optional[int] = None
    name: Optional[str] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


# ============== Responsibility Schemas ==============

class ResponsibilityBase(BaseModel):
    experience_id: int
    description: str = Field(..., min_length=1)


class ResponsibilityCreate(MySQLEntity):
    experience_id: int
    description: str = Field(..., min_length=1)

    @classmethod
    def get_table_name(cls) -> str:
        return "responsibilities"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"experience_id": "experience_id", "description": "description"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        query = "INSERT INTO responsibilities (experience_id, description) VALUES (%s, %s)"
        params = (self.experience_id, self.description)
        return (query, params)

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        query = "UPDATE responsibilities SET experience_id = %s, description = %s WHERE id = %s"
        params = (self.experience_id, self.description, entity_id)
        return (query, params)


class ResponsibilityUpdate(MySQLEntity):
    experience_id: Optional[int] = None
    description: Optional[str] = Field(None, min_length=1)

    @classmethod
    def get_table_name(cls) -> str:
        return "responsibilities"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"experience_id": "experience_id", "description": "description"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        raise NotImplementedError("Update schema should not be used for insert operations")

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        updates = []
        params = []

        if self.experience_id is not None:
            updates.append("experience_id = %s")
            params.append(self.experience_id)
        if self.description is not None:
            updates.append("description = %s")
            params.append(self.description)

        if not updates:
            raise ValueError("No fields to update")

        query = f"UPDATE responsibilities SET {', '.join(updates)} WHERE id = %s"
        params.append(entity_id)
        return (query, tuple(params))


class ResponsibilityResponse(ResponsibilityBase):
    id: int

    class Config:
        from_attributes = True


class ResponsibilityQuery(BaseModel):
    experience_id: Optional[int] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


# ============== Technology Project (Many-to-Many) Schemas ==============

class TechnologyProjectBase(BaseModel):
    technology_id: int
    project_id: int


class TechnologyProjectCreate(MySQLEntity):
    technology_id: int
    project_id: int

    @classmethod
    def get_table_name(cls) -> str:
        return "technology_projects"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"technology_id": "technology_id", "project_id": "project_id"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        query = "INSERT INTO technology_projects (technology_id, project_id) VALUES (%s, %s)"
        params = (self.technology_id, self.project_id)
        return (query, params)

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        query = "UPDATE technology_projects SET technology_id = %s, project_id = %s WHERE id = %s"
        params = (self.technology_id, self.project_id, entity_id)
        return (query, params)


class TechnologyProjectResponse(TechnologyProjectBase):
    id: int

    class Config:
        from_attributes = True


class TechnologyProjectQuery(BaseModel):
    technology_id: Optional[int] = None
    project_id: Optional[int] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


# ============== Company Experience (Many-to-Many) Schemas ==============

class CompanyExperienceBase(BaseModel):
    company_id: int
    experience_id: int


class CompanyExperienceCreate(MySQLEntity):
    company_id: int
    experience_id: int

    @classmethod
    def get_table_name(cls) -> str:
        return "company_experiences"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"company_id": "company_id", "experience_id": "experience_id"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        query = "INSERT INTO company_experiences (company_id, experience_id) VALUES (%s, %s)"
        params = (self.company_id, self.experience_id)
        return (query, params)

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        query = "UPDATE company_experiences SET company_id = %s, experience_id = %s WHERE id = %s"
        params = (self.company_id, self.experience_id, entity_id)
        return (query, params)


class CompanyExperienceResponse(CompanyExperienceBase):
    id: int

    class Config:
        from_attributes = True


class CompanyExperienceQuery(BaseModel):
    company_id: Optional[int] = None
    experience_id: Optional[int] = None
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)


# ============== Technology Experience (Many-to-Many) Schemas ==============

class TechnologyExperienceBase(BaseModel):
    technology_id: int
    experience_id: int


class TechnologyExperienceCreate(MySQLEntity):
    technology_id: int
    experience_id: int

    @classmethod
    def get_table_name(cls) -> str:
        return "technology_experiences"

    @classmethod
    def get_field_mappings(cls) -> Dict[str, str]:
        return {"technology_id": "technology_id", "experience_id": "experience_id"}

    def get_insert_query(self) -> Tuple[str, tuple]:
        query = "INSERT INTO technology_experiences (technology_id, experience_id) VALUES (%s, %s)"
        params = (self.technology_id, self.experience_id)
        return (query, params)

    def get_update_query(self, entity_id: int) -> Tuple[str, tuple]:
        query = "UPDATE technology_experiences SET technology_id = %s, experience_id = %s WHERE id = %s"
        params = (self.technology_id, self.experience_id, entity_id)
        return (query, params)


class TechnologyExperienceResponse(TechnologyExperienceBase):
    id: int

    class Config:
        from_attributes = True


class TechnologyExperienceQuery(BaseModel):
    technology_id: Optional[int] = None
    experience_id: Optional[int] = None
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
