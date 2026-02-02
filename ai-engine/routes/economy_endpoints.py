"""
Endpoints de Economía de Trabajo - FastAPI
Rutas para trabajos, compra de propiedades y gestión económica
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import sys
import os

# Añadir path para imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from economy_system.work_economy import (
    economy_manager,
    JobType,
    JobDifficulty,
    PropertyType
)

router = APIRouter(prefix="/api/economy", tags=["economy"])


# === MODELOS PYDANTIC ===

class StartWorkRequest(BaseModel):
    player_id: str
    shift_id: str

class CompleteWorkRequest(BaseModel):
    player_id: str
    performance_score: float = 75.0  # 0-100

class PurchasePropertyRequest(BaseModel):
    player_id: str
    property_id: str

class UpgradePropertyRequest(BaseModel):
    player_id: str
    property_id: str

class EnergyRegenRequest(BaseModel):
    player_id: str
    amount: int = 20


# === RUTAS DE TRABAJOS ===

@router.get("/jobs")
async def get_available_jobs(zone_id: Optional[str] = None):
    """
    Obtiene lista de trabajos disponibles
    Query params:
    - zone_id: Filtra por zona específica (opcional)
    """
    try:
        jobs = economy_manager.get_available_jobs(zone_id)
        return {
            "success": True,
            "total": len(jobs),
            "jobs": jobs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/work/start")
async def start_work(request: StartWorkRequest):
    """
    Inicia una sesión de trabajo
    Body:
    - player_id: ID del jugador
    - shift_id: ID del turno de trabajo
    """
    try:
        result = economy_manager.start_work_shift(request.player_id, request.shift_id)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": "Trabajo iniciado",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/work/complete")
async def complete_work(request: CompleteWorkRequest):
    """
    Completa el trabajo actual del jugador
    Body:
    - player_id: ID del jugador
    - performance_score: Puntuación de rendimiento 0-100 (default: 75)
    """
    try:
        player = economy_manager.get_player(request.player_id)
        result = player.complete_work(request.performance_score)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": "Trabajo completado",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/work/status/{player_id}")
async def get_work_status(player_id: str):
    """
    Obtiene el estado de trabajo actual del jugador
    """
    try:
        player = economy_manager.get_player(player_id)
        
        if player.active_work_session:
            return {
                "success": True,
                "is_working": True,
                "session": player.active_work_session.to_dict()
            }
        else:
            return {
                "success": True,
                "is_working": False,
                "message": "No hay trabajo activo"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === RUTAS DE PROPIEDADES ===

@router.get("/properties/available")
async def get_available_properties(
    zone_id: Optional[str] = None,
    property_type: Optional[str] = None
):
    """
    Obtiene propiedades disponibles para compra
    Query params:
    - zone_id: Filtra por zona (opcional)
    - property_type: Filtra por tipo de propiedad (opcional)
    """
    try:
        prop_type = None
        if property_type:
            try:
                prop_type = PropertyType[property_type.upper()]
            except KeyError:
                raise HTTPException(status_code=400, detail=f"Tipo de propiedad inválido: {property_type}")
        
        properties = economy_manager.get_available_properties(zone_id, prop_type)
        
        return {
            "success": True,
            "total": len(properties),
            "properties": properties
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/properties/owned/{player_id}")
async def get_player_properties(player_id: str):
    """
    Obtiene propiedades del jugador
    """
    try:
        properties = economy_manager.get_player_properties(player_id)
        
        return {
            "success": True,
            "player_id": player_id,
            "total": len(properties),
            "properties": properties
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/properties/purchase")
async def purchase_property(request: PurchasePropertyRequest):
    """
    Compra una propiedad
    Body:
    - player_id: ID del jugador
    - property_id: ID de la propiedad
    """
    try:
        player = economy_manager.get_player(request.player_id)
        property_obj = economy_manager.properties.get(request.property_id)
        
        if not property_obj:
            raise HTTPException(status_code=404, detail="Propiedad no encontrada")
        
        result = player.purchase_property(property_obj)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "message": "Propiedad comprada exitosamente",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/properties/upgrade")
async def upgrade_property(request: UpgradePropertyRequest):
    """
    Mejora una propiedad del jugador
    Body:
    - player_id: ID del jugador
    - property_id: ID de la propiedad
    """
    try:
        property_obj = economy_manager.properties.get(request.property_id)
        
        if not property_obj:
            raise HTTPException(status_code=404, detail="Propiedad no encontrada")
        
        if property_obj.owner_id != request.player_id:
            raise HTTPException(status_code=403, detail="No eres dueño de esta propiedad")
        
        player = economy_manager.get_player(request.player_id)
        result = property_obj.upgrade()
        
        # Verificar si tiene fondos
        if player.wallet_balance < result["upgrade_cost"]:
            raise HTTPException(
                status_code=400,
                detail=f"Fondos insuficientes. Necesitas {result['upgrade_cost']} ROBOT"
            )
        
        # Cobrar mejora
        player.wallet_balance -= result["upgrade_cost"]
        player.total_spent += result["upgrade_cost"]
        
        return {
            "success": True,
            "message": "Propiedad mejorada",
            "data": result,
            "new_balance": player.wallet_balance
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === RUTAS DE ECONOMÍA DEL JUGADOR ===

@router.get("/player/{player_id}")
async def get_player_economy(player_id: str):
    """
    Obtiene información económica del jugador
    """
    try:
        player = economy_manager.get_player(player_id)
        
        return {
            "success": True,
            "player": player.to_dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/player/energy/regenerate")
async def regenerate_energy(request: EnergyRegenRequest):
    """
    Regenera energía del jugador
    Body:
    - player_id: ID del jugador
    - amount: Cantidad de energía a regenerar (default: 20)
    """
    try:
        player = economy_manager.get_player(request.player_id)
        old_energy = player.energy
        player.regenerate_energy(request.amount)
        
        return {
            "success": True,
            "old_energy": old_energy,
            "new_energy": player.energy,
            "regenerated": player.energy - old_energy
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/player/{player_id}/income/collect")
async def collect_passive_income(player_id: str):
    """
    Recolecta ingreso pasivo de propiedades del jugador
    """
    try:
        player = economy_manager.get_player(player_id)
        player_properties = [
            p for p in economy_manager.properties.values()
            if p.owner_id == player_id
        ]
        
        income = player.collect_passive_income(player_properties)
        
        return {
            "success": True,
            "income_collected": round(income, 2),
            "new_balance": round(player.wallet_balance, 2),
            "properties_count": len(player_properties)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === ESTADÍSTICAS GLOBALES ===

@router.get("/stats")
async def get_economy_stats():
    """
    Obtiene estadísticas globales de economía
    """
    try:
        stats = economy_manager.get_economy_stats()
        
        return {
            "success": True,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/leaderboard/richest")
async def get_richest_players(limit: int = 10):
    """
    Obtiene los jugadores más ricos
    Query params:
    - limit: Cantidad de jugadores a mostrar (default: 10)
    """
    try:
        players = sorted(
            economy_manager.players.values(),
            key=lambda p: p.wallet_balance,
            reverse=True
        )[:limit]
        
        leaderboard = [
            {
                "rank": i + 1,
                "player_id": p.player_id,
                "balance": round(p.wallet_balance, 2),
                "work_level": p.work_level,
                "properties": len(p.owned_properties)
            }
            for i, p in enumerate(players)
        ]
        
        return {
            "success": True,
            "leaderboard": leaderboard
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/leaderboard/workers")
async def get_top_workers(limit: int = 10):
    """
    Obtiene los mejores trabajadores por experiencia
    Query params:
    - limit: Cantidad de jugadores a mostrar (default: 10)
    """
    try:
        players = sorted(
            economy_manager.players.values(),
            key=lambda p: p.work_experience,
            reverse=True
        )[:limit]
        
        leaderboard = [
            {
                "rank": i + 1,
                "player_id": p.player_id,
                "work_experience": p.work_experience,
                "work_level": p.work_level,
                "total_earned": round(p.total_earned, 2),
                "work_sessions": len(p.work_history)
            }
            for i, p in enumerate(players)
        ]
        
        return {
            "success": True,
            "leaderboard": leaderboard
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# === INFORMACIÓN DEL SISTEMA ===

@router.get("/info/job-types")
async def get_job_types():
    """
    Obtiene información sobre los tipos de trabajos disponibles
    """
    job_info = {
        job_type.value: {
            "name": job_type.name,
            "description": f"Trabajo de {job_type.value.replace('_', ' ')}",
            "available_difficulties": [d.name for d in JobDifficulty]
        }
        for job_type in JobType
    }
    
    return {
        "success": True,
        "job_types": job_info
    }


@router.get("/info/property-types")
async def get_property_types():
    """
    Obtiene información sobre los tipos de propiedades disponibles
    """
    property_info = {
        prop_type.value: {
            "name": prop_type.name,
            "description": f"Propiedad tipo {prop_type.value.replace('_', ' ')}"
        }
        for prop_type in PropertyType
    }
    
    return {
        "success": True,
        "property_types": property_info
    }
