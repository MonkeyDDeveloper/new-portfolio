"""
FastAPI API with OAuth2 authentication and IP whitelist
"""
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from decouple import config
from typing import Optional

from database.utils.utils import verify_token
from routers import (
    auth,
    companies,
    technologies,
    experiences,
    projects,
    project_tasks,
    responsibilities,
    technology_projects,
    company_experiences,
    technology_experiences
)

# Security scheme for Swagger UI
security = HTTPBearer(auto_error=False)

# Dependency for OpenAPI documentation (actual validation done by middleware)
async def swagger_security(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """This dependency only exists for Swagger UI documentation - actual auth is handled by middleware"""
    return credentials

app = FastAPI(
    title="Portfolio API",
    description="Portfolio API with OAuth2 authentication, companies, technologies, experiences, and projects",
    version="1.0.0"
)

PUBLIC_PATHS = [
    "/auth",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health",
]


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "API running correctly"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
@app.middleware("http")
async def verify_token_middleware(request: Request, call_next):
    if any(request.url.path.startswith(path) for path in PUBLIC_PATHS):
        return await call_next(request)
    white_list_ips = config("WHITELISTED_IPS").split(",")
    if request.client.host in white_list_ips:
        return await call_next(request)
    headers = request.headers
    bearer_token = headers.get("authorization")
    valid_token = verify_token(token=bearer_token)
    if valid_token:
        return await call_next(request)
    return JSONResponse({"detail": "Invalid token"}, status_code=HTTP_401_UNAUTHORIZED)
# Portfolio Entities
app.include_router(companies.router, prefix="/companies", tags=["Companies"], dependencies=[Depends(swagger_security)])
app.include_router(technologies.router, prefix="/technologies", tags=["Technologies"], dependencies=[Depends(swagger_security)])
app.include_router(experiences.router, prefix="/experiences", tags=["Professional Experiences"], dependencies=[Depends(swagger_security)])
app.include_router(projects.router, prefix="/projects", tags=["Projects"], dependencies=[Depends(swagger_security)])
app.include_router(project_tasks.router, prefix="/project-tasks", tags=["Project Tasks"], dependencies=[Depends(swagger_security)])
app.include_router(responsibilities.router, prefix="/responsibilities", tags=["Responsibilities"], dependencies=[Depends(swagger_security)])

# Many-to-Many Relations
app.include_router(technology_projects.router, prefix="/technology-projects", tags=["Technology-Project Relations"], dependencies=[Depends(swagger_security)])
app.include_router(company_experiences.router, prefix="/company-experiences", tags=["Company-Experience Relations"], dependencies=[Depends(swagger_security)])
app.include_router(technology_experiences.router, prefix="/technology-experiences", tags=["Technology-Experience Relations"], dependencies=[Depends(swagger_security)])
