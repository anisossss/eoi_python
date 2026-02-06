"""
CSIR EOI 8119 - Mining Analytics API (Demo)
Vercel Serverless Function
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(
    title="CSIR Mining Analytics API",
    description="Mining Data Analytics API - CSIR EOI 8119/06/02/2026",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "CSIR Mining Analytics API",
        "version": "1.0.0",
        "eoi": "8119/06/02/2026",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/api/health")
def health():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/production/summary")
def production_summary():
    """Demo endpoint - Production Summary"""
    return {
        "total_ore_tonnes": 15420.5,
        "total_waste_tonnes": 8230.2,
        "average_grade": 2.85,
        "active_equipment": 12,
        "shifts_today": 3,
        "workers_on_shift": 145
    }

@app.get("/api/equipment")
def equipment_list():
    """Demo endpoint - Equipment List"""
    return {
        "equipment": [
            {"id": 1, "code": "EQ-001", "name": "Drill Rig Alpha", "status": "operational"},
            {"id": 2, "code": "EQ-002", "name": "Haul Truck Beta", "status": "operational"},
            {"id": 3, "code": "EQ-003", "name": "Loader Gamma", "status": "maintenance"},
        ]
    }

@app.get("/api/shifts")
def shifts_list():
    """Demo endpoint - Shifts"""
    return {
        "shifts": [
            {"id": 1, "date": "2026-02-06", "type": "day", "workers": 48},
            {"id": 2, "date": "2026-02-06", "type": "afternoon", "workers": 52},
            {"id": 3, "date": "2026-02-06", "type": "night", "workers": 45},
        ]
    }

# Handler for Vercel
handler = app
