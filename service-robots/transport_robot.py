"""
🚌 Robot Transporte — Puerto 8003
Gestión de rutas, entregas y rastreo en tiempo real.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
import uvicorn
import uuid
import os

app = FastAPI(
    title="Robot Transporte 🚌",
    description="Sistema de transporte y logística robótica para Ciudad Robot",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

web_dir = os.path.join(os.path.dirname(__file__), "web")
if os.path.isdir(web_dir):
    app.mount("/web", StaticFiles(directory=web_dir), name="web")


# ── Models ──────────────────────────────────────────────────────────────────

class TransportRequest(BaseModel):
    pickup_location: str
    destination: str
    cargo_type: str  # person | package | food | medical | fragile
    contact_name: str
    contact_phone: Optional[str] = None
    notes: Optional[str] = None


# ── In-memory storage ────────────────────────────────────────────────────────

transport_requests: dict[str, dict] = {}

available_routes = [
    {"id": "R01", "name": "Ruta Norte-Sur", "distance_km": 12, "estimated_minutes": 25, "status": "activa"},
    {"id": "R02", "name": "Ruta Centro-Aeropuerto", "distance_km": 18, "estimated_minutes": 35, "status": "activa"},
    {"id": "R03", "name": "Ruta Costera", "distance_km": 8, "estimated_minutes": 20, "status": "activa"},
    {"id": "R04", "name": "Ruta Industrial", "distance_km": 22, "estimated_minutes": 40, "status": "mantenimiento"},
    {"id": "R05", "name": "Ruta Suburbana", "distance_km": 15, "estimated_minutes": 30, "status": "activa"},
]


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "online",
        "robot": "Robot Transporte",
        "port": 8003,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
def root():
    return FileResponse(os.path.join(web_dir, "transport.html"))


@app.post("/api/transport/request")
def request_transport(req: TransportRequest):
    request_id = str(uuid.uuid4())
    entry = {
        "id": request_id,
        "pickup_location": req.pickup_location,
        "destination": req.destination,
        "cargo_type": req.cargo_type,
        "contact_name": req.contact_name,
        "contact_phone": req.contact_phone,
        "notes": req.notes,
        "status": "en_transito",
        "estimated_arrival": "25 minutos",
        "driver_unit": f"UNIT-{request_id[:4].upper()}",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    transport_requests[request_id] = entry
    return {
        "message": "🚀 Solicitud de transporte aceptada.",
        "request": entry,
    }


@app.get("/api/transport/routes")
def get_routes():
    return {
        "routes": available_routes,
        "active_routes": len([r for r in available_routes if r["status"] == "activa"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/transport/track/{id}")
def track_transport(id: str):
    entry = transport_requests.get(id)
    if not entry:
        raise HTTPException(status_code=404, detail="Solicitud de transporte no encontrada")
    return {
        "tracking": {
            "id": entry["id"],
            "status": entry["status"],
            "current_location": "En ruta — 10 km del destino",
            "estimated_arrival": entry["estimated_arrival"],
            "driver_unit": entry["driver_unit"],
            "destination": entry["destination"],
            "last_updated": datetime.now(timezone.utc).isoformat(),
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
