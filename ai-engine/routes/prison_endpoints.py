"""
Endpoints de Cárcel y Rehabilitación
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from security_system.prison_system import prison_manager

router = APIRouter(prefix="/api/prison", tags=["prison"])


class SentenceRequest(BaseModel):
    player_id: str
    reason: str
    duration_minutes: int


class BehaviorRequest(BaseModel):
    player_id: str
    points: int = 1


class WorkRequest(BaseModel):
    player_id: str
    minutes: int


class TickRequest(BaseModel):
    player_id: str
    minutes: int = 1


@router.post("/sentence")
async def sentence_player(request: SentenceRequest):
    if request.duration_minutes <= 0:
        raise HTTPException(status_code=400, detail="Invalid duration")
    sentence = prison_manager.sentence_player(
        request.player_id,
        request.reason,
        request.duration_minutes
    )
    return {"sentence": sentence.to_dict()}


@router.get("/inmates")
async def get_active_inmates():
    return {"inmates": prison_manager.get_active_inmates()}


@router.get("/inmates/{player_id}")
async def get_inmate(player_id: str):
    sentence = prison_manager.get_inmate_sentence(player_id)
    if not sentence:
        raise HTTPException(status_code=404, detail="Inmate not found")
    return {"sentence": sentence.to_dict()}


@router.post("/behavior")
async def add_good_behavior(request: BehaviorRequest):
    sentence = prison_manager.add_good_behavior(request.player_id, request.points)
    if not sentence:
        raise HTTPException(status_code=404, detail="Inmate not found")
    return {"sentence": sentence.to_dict()}


@router.post("/work")
async def add_voluntary_work(request: WorkRequest):
    if request.minutes <= 0:
        raise HTTPException(status_code=400, detail="Invalid minutes")
    sentence = prison_manager.add_voluntary_work(request.player_id, request.minutes)
    if not sentence:
        raise HTTPException(status_code=404, detail="Inmate not found")
    return {"sentence": sentence.to_dict()}


@router.post("/tick")
async def tick_sentence(request: TickRequest):
    sentence = prison_manager.tick_sentence(request.player_id, request.minutes)
    if not sentence:
        raise HTTPException(status_code=404, detail="Inmate not found")
    return {"sentence": sentence.to_dict()}


@router.post("/release/{player_id}")
async def release_player(player_id: str):
    sentence = prison_manager.release_player(player_id)
    if not sentence:
        raise HTTPException(status_code=404, detail="Inmate not found")
    return {"sentence": sentence.to_dict()}
