"""
🚔 Robot Policía — Puerto 8002
Seguridad, patrullaje y gestión de incidentes para la vida real.
"""

from fastapi import FastAPI
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
    title="Robot Policía 🚔",
    description="Sistema de seguridad y patrullaje robótico para Ciudad Robot",
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

class AlertRequest(BaseModel):
    location: str
    alert_type: str  # theft | vandalism | accident | fire | suspicious
    description: str
    reporter_name: Optional[str] = None
    contact_phone: Optional[str] = None


class IncidentReport(BaseModel):
    incident_type: str
    location: str
    description: str
    involved_parties: Optional[str] = None
    reporter_name: Optional[str] = None
    contact_phone: Optional[str] = None


# ── In-memory storage ────────────────────────────────────────────────────────

alerts: list[dict] = []
incidents: list[dict] = []

patrol_zones = [
    {"zone": "Zona Norte", "status": "patrullando", "unit": "Unidad-01"},
    {"zone": "Zona Sur", "status": "patrullando", "unit": "Unidad-02"},
    {"zone": "Zona Centro", "status": "disponible", "unit": "Unidad-03"},
    {"zone": "Zona Este", "status": "respondiendo", "unit": "Unidad-04"},
]


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "online",
        "robot": "Robot Policía",
        "port": 8002,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
def root():
    return FileResponse(os.path.join(web_dir, "security.html"))


@app.post("/api/security/alert")
def send_alert(req: AlertRequest):
    alert = {
        "id": str(uuid.uuid4()),
        "location": req.location,
        "alert_type": req.alert_type,
        "description": req.description,
        "reporter_name": req.reporter_name,
        "contact_phone": req.contact_phone,
        "status": "respondiendo",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    alerts.append(alert)
    return {
        "message": "🚨 Alerta recibida. Unidad policial en camino.",
        "alert": alert,
    }


@app.get("/api/security/patrol-status")
def patrol_status():
    return {
        "patrol_zones": patrol_zones,
        "active_alerts": len([a for a in alerts if a["status"] == "respondiendo"]),
        "total_incidents": len(incidents),
        "officers_on_duty": 8,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/security/report")
def report_incident(req: IncidentReport):
    incident = {
        "id": str(uuid.uuid4()),
        "incident_type": req.incident_type,
        "location": req.location,
        "description": req.description,
        "involved_parties": req.involved_parties,
        "reporter_name": req.reporter_name,
        "contact_phone": req.contact_phone,
        "status": "en_investigacion",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    incidents.append(incident)
    return {
        "message": "📋 Reporte de incidente registrado.",
        "incident": incident,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
