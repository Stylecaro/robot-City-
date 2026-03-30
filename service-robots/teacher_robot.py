"""
🎓 Robot Maestro — Puerto 8006
Plataforma educativa automatizada con cursos y lecciones interactivas.
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
    title="Robot Maestro 🎓",
    description="Plataforma educativa robótica para Ciudad Robot",
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

class EnrollRequest(BaseModel):
    student_name: str
    course_id: str
    email: Optional[str] = None
    experience_level: str = "beginner"  # beginner | intermediate | advanced


# ── In-memory storage ────────────────────────────────────────────────────────

enrollments: list[dict] = []

course_catalog = [
    {
        "id": "C001",
        "title": "Robótica para Principiantes",
        "level": "beginner",
        "duration_hours": 20,
        "topics": ["Introducción a robots", "Sensores básicos", "Programación Arduino"],
        "instructor": "Robot Maestro v1",
        "enrolled": 142,
    },
    {
        "id": "C002",
        "title": "Programación con Python",
        "level": "beginner",
        "duration_hours": 30,
        "topics": ["Variables", "Bucles", "Funciones", "POO"],
        "instructor": "Robot Maestro v1",
        "enrolled": 230,
    },
    {
        "id": "C003",
        "title": "Inteligencia Artificial Aplicada",
        "level": "intermediate",
        "duration_hours": 40,
        "topics": ["Machine Learning", "Redes Neuronales", "Computer Vision"],
        "instructor": "Robot Maestro v2",
        "enrolled": 87,
    },
    {
        "id": "C004",
        "title": "IoT con Raspberry Pi",
        "level": "intermediate",
        "duration_hours": 25,
        "topics": ["GPIO", "Sensores IoT", "MQTT", "Dashboards"],
        "instructor": "Robot Maestro v1",
        "enrolled": 65,
    },
    {
        "id": "C005",
        "title": "Computación Cuántica",
        "level": "advanced",
        "duration_hours": 50,
        "topics": ["Qubits", "Circuitos cuánticos", "Algoritmos QAOA"],
        "instructor": "Robot Maestro v3",
        "enrolled": 23,
    },
]

lesson_library = {
    "C001-L01": {
        "id": "C001-L01",
        "course_id": "C001",
        "title": "¿Qué es un Robot?",
        "content": "Un robot es una máquina programable capaz de realizar tareas de forma autónoma. Los robots modernos combinan sensores, actuadores y software de IA para interactuar con el mundo real.",
        "duration_minutes": 30,
        "resources": ["video_intro.mp4", "slides_01.pdf"],
    },
    "C002-L01": {
        "id": "C002-L01",
        "course_id": "C002",
        "title": "Variables y Tipos de Datos en Python",
        "content": "En Python, las variables son contenedores para almacenar datos. Los tipos principales son: int (enteros), float (decimales), str (texto) y bool (verdadero/falso).",
        "duration_minutes": 45,
        "resources": ["ejercicio_variables.py", "slides_python_01.pdf"],
    },
    "C003-L01": {
        "id": "C003-L01",
        "course_id": "C003",
        "title": "Introducción al Machine Learning",
        "content": "Machine Learning permite que los sistemas aprendan y mejoren automáticamente a partir de la experiencia sin ser explícitamente programados para cada tarea.",
        "duration_minutes": 60,
        "resources": ["notebook_ml_intro.ipynb", "dataset_ejemplo.csv"],
    },
}


# ── Routes ───────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "online",
        "robot": "Robot Maestro",
        "port": 8006,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/")
def root():
    return FileResponse(os.path.join(web_dir, "teacher.html"))


@app.get("/api/teacher/courses")
def list_courses(level: Optional[str] = None):
    courses = course_catalog
    if level:
        courses = [c for c in course_catalog if c["level"] == level]
    return {
        "courses": courses,
        "total": len(courses),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/teacher/enroll")
def enroll(req: EnrollRequest):
    course = next((c for c in course_catalog if c["id"] == req.course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Curso no encontrado")

    enrollment = {
        "id": str(uuid.uuid4()),
        "student_name": req.student_name,
        "course_id": req.course_id,
        "course_title": course["title"],
        "email": req.email,
        "experience_level": req.experience_level,
        "status": "activo",
        "progress_percent": 0,
        "enrolled_at": datetime.now(timezone.utc).isoformat(),
    }
    course["enrolled"] += 1
    enrollments.append(enrollment)
    return {
        "message": f"🎓 Inscripción confirmada en '{course['title']}'.",
        "enrollment": enrollment,
    }


@app.get("/api/teacher/lesson/{id}")
def get_lesson(id: str):
    lesson = lesson_library.get(id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lección no encontrada")
    return {"lesson": lesson}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)
