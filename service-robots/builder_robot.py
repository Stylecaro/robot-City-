"""
🏗️ Robot Constructor — Puerto 8005
Gestión de proyectos de construcción automatizados.
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
    title="Robot Constructor 🏗️",
    description="Sistema de gestión de proyectos de construcción para Ciudad Robot",
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

class ProjectRequest(BaseModel):
    project_name: str
    project_type: str  # residential | commercial | infrastructure | industrial
    location: str
    budget: float
    start_date: str
    description: Optional[str] = None
    client_name: Optional[str] = None


class ProgressUpdate(BaseModel):
    progress_percent: int  # 0–100
    notes: Optional[str] = None


# ── In-memory storage ────────────────────────────────────────────────────────

projects: dict[str, dict] = {}


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "online",
        "robot": "Robot Constructor",
        "port": 8005,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
def root():
    return FileResponse(os.path.join(web_dir, "builder.html"))


@app.post("/api/builder/project")
def create_project(req: ProjectRequest):
    project_id = str(uuid.uuid4())
    project = {
        "id": project_id,
        "project_name": req.project_name,
        "project_type": req.project_type,
        "location": req.location,
        "budget": req.budget,
        "start_date": req.start_date,
        "description": req.description,
        "client_name": req.client_name,
        "status": "en_progreso",
        "progress_percent": 0,
        "robots_assigned": 2,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    projects[project_id] = project
    return {
        "message": "🏗️ Proyecto de construcción creado.",
        "project": project,
    }


@app.get("/api/builder/projects")
def list_projects():
    return {
        "projects": list(projects.values()),
        "total": len(projects),
        "active": len([p for p in projects.values() if p["status"] == "en_progreso"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.put("/api/builder/project/{id}/progress")
def update_progress(id: str, req: ProgressUpdate):
    project = projects.get(id)
    if not project:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    project["progress_percent"] = req.progress_percent
    if req.notes:
        project["last_update_notes"] = req.notes
    if req.progress_percent >= 100:
        project["status"] = "completado"
    project["updated_at"] = datetime.now(timezone.utc).isoformat()
    return {
        "message": f"📊 Progreso actualizado al {req.progress_percent}%.",
        "project": project,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
