"""
Router de proyectos
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db, Project
from schemas import ProjectCreate, ProjectUpdate, ProjectResponse, MessageResponse
from auth import get_current_client_or_whitelisted

router = APIRouter()


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED, summary="Crear proyecto")
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Crear un nuevo proyecto.
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    new_project = Project(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("", response_model=List[ProjectResponse], summary="Listar proyectos")
async def list_projects(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros"),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Listar todos los proyectos con paginación.
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects


@router.get("/search", response_model=List[ProjectResponse], summary="Buscar proyectos")
async def search_projects(
    title: Optional[str] = Query(None, description="Buscar por título (parcial)"),
    status: Optional[str] = Query(None, description="Filtrar por estado"),
    tags: Optional[str] = Query(None, description="Filtrar por tags (parcial)"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Buscar proyectos con filtros.
    
    - **title**: Búsqueda parcial en el título
    - **status**: Filtro exacto por estado
    - **tags**: Búsqueda parcial en tags
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    query = db.query(Project)
    
    if title:
        query = query.filter(Project.title.ilike(f"%{title}%"))
    if status:
        query = query.filter(Project.status == status)
    if tags:
        query = query.filter(Project.tags.ilike(f"%{tags}%"))
    
    projects = query.offset(skip).limit(limit).all()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse, summary="Obtener proyecto")
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Obtener un proyecto por su ID.
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    return project


@router.put("/{project_id}", response_model=ProjectResponse, summary="Actualizar proyecto")
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Actualizar un proyecto existente.
    
    Solo se actualizan los campos proporcionados.
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    update_data = project_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(project, field, value)
    
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", response_model=MessageResponse, summary="Eliminar proyecto")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Eliminar un proyecto.
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    db.delete(project)
    db.commit()
    
    return MessageResponse(message="Proyecto eliminado exitosamente")
