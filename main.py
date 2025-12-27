"""
FastAPI API with OAuth2 authentication and IP whitelist
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth


app = FastAPI(
    title="Projects and Blogs API",
    description="API with OAuth2 authentication and IP whitelist",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "API running correctly"}


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}
