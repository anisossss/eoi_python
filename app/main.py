"""
Main Application
CSIR EOI 8119 - Mining Data Analytics API

Demonstrates proficiency in:
- Python (FastAPI framework)
- PostgreSQL (relational database)
- REST API development
- Background processing (Celery)
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.db.database import init_db
from app.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    # Startup: Initialize database tables
    init_db()
    yield
    # Shutdown: Cleanup if needed
    pass


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="""
## CSIR EOI 8119 - Mining Data Analytics API

This API demonstrates proficiency in:
- **Python** with FastAPI framework
- **PostgreSQL** relational database
- **SQL queries** with aggregations and joins
- **Background processing** with Celery
- **Docker** containerization

### Features
- Mining shift management
- Production data tracking
- Equipment registry
- Maintenance logging
- Analytics and reporting

### Technical Stack
- FastAPI + Uvicorn
- PostgreSQL + SQLAlchemy
- Celery + Redis
- Docker + Docker Compose
    """,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")


@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Mining Data Analytics API for CSIR EOI 8119",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
