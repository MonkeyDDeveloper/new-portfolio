"""
Router de blogs
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db, Blog
from schemas import BlogCreate, BlogUpdate, BlogResponse, MessageResponse
from auth import get_current_client_or_whitelisted

router = APIRouter()


@router.post("", response_model=BlogResponse, status_code=status.HTTP_201_CREATED, summary="Crear blog")
async def create_blog(
    blog: BlogCreate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Crear un nuevo blog.
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    new_blog = Blog(**blog.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("", response_model=List[BlogResponse], summary="Listar blogs")
async def list_blogs(
    skip: int = Query(0, ge=0, description="Número de registros a saltar"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros"),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Listar todos los blogs con paginación.
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    blogs = db.query(Blog).offset(skip).limit(limit).all()
    return blogs


@router.get("/search", response_model=List[BlogResponse], summary="Buscar blogs")
async def search_blogs(
    title: Optional[str] = Query(None, description="Buscar por título (parcial)"),
    author: Optional[str] = Query(None, description="Filtrar por autor (parcial)"),
    tags: Optional[str] = Query(None, description="Filtrar por tags (parcial)"),
    published: Optional[bool] = Query(None, description="Filtrar por estado de publicación"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Buscar blogs con filtros.
    
    - **title**: Búsqueda parcial en el título
    - **author**: Búsqueda parcial por autor
    - **tags**: Búsqueda parcial en tags
    - **published**: Filtro por estado de publicación
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    query = db.query(Blog)
    
    if title:
        query = query.filter(Blog.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Blog.author.ilike(f"%{author}%"))
    if tags:
        query = query.filter(Blog.tags.ilike(f"%{tags}%"))
    if published is not None:
        query = query.filter(Blog.published == published)
    
    blogs = query.offset(skip).limit(limit).all()
    return blogs


@router.get("/{blog_id}", response_model=BlogResponse, summary="Obtener blog")
async def get_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Obtener un blog por su ID.
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog no encontrado"
        )
    return blog


@router.put("/{blog_id}", response_model=BlogResponse, summary="Actualizar blog")
async def update_blog(
    blog_id: int,
    blog_data: BlogUpdate,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Actualizar un blog existente.
    
    Solo se actualizan los campos proporcionados.
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog no encontrado"
        )
    
    update_data = blog_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(blog, field, value)
    
    db.commit()
    db.refresh(blog)
    return blog


@router.delete("/{blog_id}", response_model=MessageResponse, summary="Eliminar blog")
async def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Eliminar un blog.
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog no encontrado"
        )
    
    db.delete(blog)
    db.commit()
    
    return MessageResponse(message="Blog eliminado exitosamente")


@router.patch("/{blog_id}/publish", response_model=BlogResponse, summary="Publicar/Despublicar blog")
async def toggle_publish_blog(
    blog_id: int,
    publish: bool = Query(..., description="True para publicar, False para despublicar"),
    db: Session = Depends(get_db),
    _: dict = Depends(get_current_client_or_whitelisted)
):
    """
    Cambiar el estado de publicación de un blog.
    
    Requiere autenticación con token O acceso desde IP en whitelist.
    """
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog no encontrado"
        )
    
    blog.published = publish
    db.commit()
    db.refresh(blog)
    return blog
