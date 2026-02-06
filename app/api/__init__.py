# API Routes
from fastapi import APIRouter

from app.api import auth, shifts, production, equipment, maintenance, analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(shifts.router, prefix="/shifts", tags=["Mining Shifts"])
api_router.include_router(production.router, prefix="/production", tags=["Production Records"])
api_router.include_router(equipment.router, prefix="/equipment", tags=["Equipment"])
api_router.include_router(maintenance.router, prefix="/maintenance", tags=["Maintenance"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
