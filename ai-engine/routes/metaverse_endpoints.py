"""
Research, Simulation y City Zones Endpoints
Integración de laboratorios, entrenamientos y zonas de ciudad
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from research_system.research_manager import research_manager, ResearchType
from simulation_system.simulation_engine import simulation_engine, SimulationType, DifficultyLevel
from spatial_scripts.city_zones import city_manager, ZoneType

router = APIRouter(prefix="/api", tags=["research-simulation-zones"])


# ============ RESEARCH ENDPOINTS ============

class CreateLabRequest(BaseModel):
    name: str
    location: str
    research_type: str


class StartResearchRequest(BaseModel):
    lab_id: str
    tech_id: str


@router.post("/research/labs/create")
async def create_lab(request: CreateLabRequest):
    """Crea nuevo laboratorio"""
    try:
        research_type = ResearchType[request.research_type.upper()]
        lab = research_manager.create_lab(request.name, request.location, research_type)
        
        return {
            "status": "created",
            "lab": lab.to_dict()
        }
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid research type")


@router.get("/research/labs")
async def get_labs():
    """Lista todos los laboratorios"""
    labs = research_manager.get_all_labs()
    
    return {
        "total": len(labs),
        "labs": [l.to_dict() for l in labs]
    }


@router.get("/research/labs/{lab_id}")
async def get_lab(lab_id: str):
    """Obtiene detalles de laboratorio"""
    lab = research_manager.get_lab(lab_id)
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    
    return {
        "lab": lab.to_dict(),
        "progress": research_manager.get_research_progress(lab_id)
    }


@router.post("/research/labs/{lab_id}/start")
async def start_research(lab_id: str, request: StartResearchRequest):
    """Inicia investigación"""
    success, message = research_manager.start_research(lab_id, request.tech_id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return {
        "status": "research_started",
        "message": message,
        "lab": research_manager.get_lab(lab_id).to_dict()
    }


@router.get("/research/technologies")
async def get_technologies(tech_type: Optional[str] = None):
    """Lista tecnologías disponibles"""
    techs = list(research_manager.technologies.values())
    
    if tech_type:
        try:
            rt = ResearchType[tech_type.upper()]
            techs = [t for t in techs if t.research_type == rt]
        except KeyError:
            pass
    
    return {
        "total": len(techs),
        "technologies": [t.to_dict() for t in techs]
    }


@router.get("/research/stats")
async def get_research_stats():
    """Obtiene estadísticas de investigación"""
    return research_manager.get_lab_stats()


# ============ SIMULATION ENDPOINTS ============

class StartSimulationRequest(BaseModel):
    robot_id: str
    scenario_id: str
    robot_stats: dict


@router.get("/simulation/scenarios")
async def get_scenarios(sim_type: Optional[str] = None, difficulty: Optional[str] = None):
    """Lista escenarios de simulación"""
    scenarios = simulation_engine.get_all_scenarios()
    
    if sim_type:
        try:
            st = SimulationType[sim_type.upper()]
            scenarios = simulation_engine.get_scenarios_by_type(st)
        except KeyError:
            pass
    
    if difficulty:
        try:
            dl = DifficultyLevel[difficulty.upper()]
            scenarios = simulation_engine.get_scenarios_by_difficulty(dl)
        except KeyError:
            pass
    
    return {
        "total": len(scenarios),
        "scenarios": [s.to_dict() for s in scenarios]
    }


@router.get("/simulation/scenarios/{scenario_id}")
async def get_scenario(scenario_id: str):
    """Obtiene detalles de escenario"""
    scenario = simulation_engine.get_scenario(scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    return scenario.to_dict()


@router.post("/simulation/start")
async def start_simulation(request: StartSimulationRequest):
    """Inicia simulación"""
    scenario = simulation_engine.get_scenario(request.scenario_id)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
    
    result = simulation_engine.simulate_performance(
        request.robot_id,
        request.scenario_id,
        request.robot_stats
    )
    
    return {
        "status": "completed" if result.completed else "failed",
        "result": result.to_dict()
    }


@router.get("/simulation/robot/{robot_id}/stats")
async def get_robot_simulation_stats(robot_id: str):
    """Obtiene estadísticas de entrenamiento de robot"""
    return simulation_engine.get_robot_stats(robot_id)


@router.get("/simulation/leaderboard")
async def get_simulation_leaderboard(limit: int = 50):
    """Obtiene leaderboard de entrenamiento"""
    return {
        "leaderboard": simulation_engine.get_leaderboard(limit)
    }


@router.get("/simulation/stats")
async def get_simulation_stats():
    """Obtiene estadísticas globales de simulaciones"""
    return simulation_engine.get_global_stats()


# ============ CITY ZONES ENDPOINTS ============

class EnterZoneRequest(BaseModel):
    player_id: str
    zone_id: str


class PlayGameRequest(BaseModel):
    player_id: str
    game_id: str


@router.get("/city/zones")
async def get_zones(zone_type: Optional[str] = None):
    """Lista zonas de la ciudad"""
    zones = city_manager.get_all_zones()
    
    if zone_type:
        try:
            zt = ZoneType[zone_type.upper()]
            zones = city_manager.get_zones_by_type(zt)
        except KeyError:
            pass
    
    return {
        "total": len(zones),
        "zones": [z.to_dict() for z in zones]
    }


@router.get("/city/zones/{zone_id}")
async def get_zone(zone_id: str):
    """Obtiene información detallada de zona"""
    info = city_manager.get_zone_info(zone_id)
    
    if not info:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    return info


@router.post("/city/zones/enter")
async def enter_zone(request: EnterZoneRequest):
    """Entra a una zona"""
    success, message = city_manager.enter_zone(request.player_id, request.zone_id)
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    zone = city_manager.get_zone(request.zone_id)
    
    return {
        "status": "entered",
        "message": message,
        "zone": zone.to_dict()
    }


@router.post("/city/zones/{zone_id}/exit")
async def exit_zone(zone_id: str, player_id: str):
    """Sale de una zona"""
    if not city_manager.exit_zone(player_id):
        raise HTTPException(status_code=400, detail="Could not exit zone")
    
    return {
        "status": "exited",
        "player_id": player_id
    }


@router.get("/city/zones/{zone_id}/games")
async def get_zone_games(zone_id: str):
    """Obtiene mini-games de una zona"""
    zone = city_manager.get_zone(zone_id)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    
    return {
        "zone_name": zone.name,
        "games": [g.to_dict() for g in zone.mini_games]
    }


@router.post("/city/zones/{zone_id}/play/{game_id}")
async def play_game(zone_id: str, game_id: str, player_id: str):
    """Inicia mini-juego en zona"""
    result = city_manager.play_mini_game(player_id, zone_id, game_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Game not found")
    
    return result


@router.get("/city/stats")
async def get_city_stats():
    """Obtiene estadísticas de la ciudad"""
    return city_manager.get_city_stats()


@router.get("/city/player/{player_id}/location")
async def get_player_location(player_id: str):
    """Obtiene zona actual del jugador"""
    zone = city_manager.get_player_zone(player_id)
    
    if not zone:
        return {
            "player_id": player_id,
            "location": None,
            "message": "Player not in any zone"
        }
    
    return {
        "player_id": player_id,
        "location": zone.name,
        "zone_id": zone.zone_id,
        "zone_info": zone.to_dict()
    }


# ============ INTEGRATED ENDPOINTS ============

@router.get("/metaverse/complete-status")
async def get_metaverse_status():
    """Obtiene estado completo del metaverso"""
    return {
        "research": research_manager.get_lab_stats(),
        "simulations": simulation_engine.get_global_stats(),
        "city": city_manager.get_city_stats(),
        "timestamp": str(__import__('datetime').datetime.now())
    }
