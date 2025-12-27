"""
API de FastAPI con autenticación OAuth2 y whitelist de IPs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import create_tables
from routers import auth, projects, blogs


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(
    title="API de Proyectos y Blogs",
    description="API con autenticación OAuth2 y whitelist de IPs",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
app.include_router(projects.router, prefix="/projects", tags=["Proyectos"])
app.include_router(blogs.router, prefix="/blogs", tags=["Blogs"])


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "API funcionando correctamente"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
