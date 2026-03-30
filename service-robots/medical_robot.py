"""
🏥 Robot Médico — Puerto 8001
Asistencia sanitaria y teleasistencia médica para la vida real.
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
    title="Robot Médico 🏥",
    description="Sistema de asistencia médica robótica para Ciudad Robot",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static web files
web_dir = os.path.join(os.path.dirname(__file__), "web")
if os.path.isdir(web_dir):
    app.mount("/web", StaticFiles(directory=web_dir), name="web")


# ── Models ──────────────────────────────────────────────────────────────────

class EmergencyRequest(BaseModel):
    patient_name: str
    location: str
    description: str
    severity: str = "medium"  # low | medium | high | critical
    contact_phone: Optional[str] = None


class AppointmentRequest(BaseModel):
    patient_name: str
    doctor_type: str
    preferred_date: str
    symptoms: Optional[str] = None
    contact_phone: Optional[str] = None


# ── In-memory storage ────────────────────────────────────────────────────────

emergencies: list[dict] = []
appointments: list[dict] = []


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "online",
        "robot": "Robot Médico",
        "port": 8001,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
def root():
    return FileResponse(os.path.join(web_dir, "medical.html"))


@app.post("/api/medical/emergency")
def report_emergency(req: EmergencyRequest):
    emergency = {
        "id": str(uuid.uuid4()),
        "patient_name": req.patient_name,
        "location": req.location,
        "description": req.description,
        "severity": req.severity,
        "contact_phone": req.contact_phone,
        "status": "dispatched",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    emergencies.append(emergency)
    return {
        "message": "🚑 Emergencia registrada. Unidad médica en camino.",
        "emergency": emergency,
    }


@app.get("/api/medical/status")
def health_status():
    return {
        "robot_status": "operativo",
        "active_emergencies": len([e for e in emergencies if e["status"] == "dispatched"]),
        "total_emergencies": len(emergencies),
        "pending_appointments": len(appointments),
        "ambulances_available": 3,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/medical/appointment")
def request_appointment(req: AppointmentRequest):
    appointment = {
        "id": str(uuid.uuid4()),
        "patient_name": req.patient_name,
        "doctor_type": req.doctor_type,
        "preferred_date": req.preferred_date,
        "symptoms": req.symptoms,
        "contact_phone": req.contact_phone,
        "status": "confirmed",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    appointments.append(appointment)
    return {
        "message": "📅 Cita médica confirmada.",
        "appointment": appointment,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
