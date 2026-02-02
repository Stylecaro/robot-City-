"""
Research System - Sistema de Investigación y Laboratorios
Mejora de tecnología, desarrollos, recursos para robots
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import uuid
import json


class ResearchType(Enum):
    """Tipos de investigación"""
    WEAPON = "weapon"              # Armas mejoradas
    ARMOR = "armor"                # Blindaje avanzado
    ENGINE = "engine"              # Motores más rápidos
    BATTERY = "battery"            # Baterías de mayor capacidad
    AI = "ai"                      # IA mejorada (inteligencia)
    SENSOR = "sensor"              # Sensores (evasión)
    SPECIAL = "special"            # Habilidades especiales
    HEALING = "healing"            # Sistemas de reparación
    COMMUNICATION = "communication" # Comunicación cuántica


class ResearchTier(Enum):
    """Niveles de investigación"""
    TIER1 = 1  # Básico
    TIER2 = 2  # Intermedio
    TIER3 = 3  # Avanzado
    TIER4 = 4  # Experto
    TIER5 = 5  # Legendario


@dataclass
class Technology:
    """Tecnología investigable"""
    tech_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    research_type: ResearchType = ResearchType.WEAPON
    tier: ResearchTier = ResearchTier.TIER1
    
    # Requisitos
    required_resources: Dict[str, int] = field(default_factory=dict)  # {"credits": 1000, "materials": 50}
    required_time_hours: float = 1.0
    prerequisites: List[str] = field(default_factory=list)  # tech_ids necesarios
    
    # Beneficios
    stat_bonus: Dict[str, int] = field(default_factory=dict)  # {"attack": 10, "speed": 5}
    
    # Estado
    progress_percent: float = 0.0
    completed: bool = False
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        return {
            "tech_id": self.tech_id,
            "name": self.name,
            "type": self.research_type.value,
            "tier": self.tier.value,
            "progress": self.progress_percent,
            "completed": self.completed,
            "stat_bonus": self.stat_bonus
        }


@dataclass
class ResearchLab:
    """Laboratorio de investigación"""
    lab_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    location: str = ""  # Zona de la ciudad
    research_type: ResearchType = ResearchType.WEAPON
    level: int = 1
    capacity: int = 3  # Proyectos simultáneos
    
    # Proyectos
    active_projects: List[str] = field(default_factory=list)  # tech_ids
    completed_projects: List[str] = field(default_factory=list)
    
    # Recursos
    credits: int = 0
    materials: int = 0
    
    # Bonificadores
    research_speed_bonus: float = 1.0  # 1.0 = normal
    success_rate_bonus: float = 1.0
    
    # Estado
    created_at: datetime = field(default_factory=datetime.now)
    
    def can_start_project(self) -> bool:
        """Verifica si puede iniciar nuevo proyecto"""
        return len(self.active_projects) < self.capacity
    
    def to_dict(self) -> Dict:
        return {
            "lab_id": self.lab_id,
            "name": self.name,
            "location": self.location,
            "type": self.research_type.value,
            "level": self.level,
            "active_projects": len(self.active_projects),
            "completed_projects": len(self.completed_projects),
            "credits": self.credits,
            "materials": self.materials
        }


class ResearchManager:
    """Gestor de investigación y laboratorios"""
    
    def __init__(self):
        self.labs: Dict[str, ResearchLab] = {}
        self.technologies: Dict[str, Technology] = {}
        self.tech_tree: Dict[str, List[str]] = {}  # tech_id -> techs desbloqueadas
        
        # Plantillas de tecnologías
        self._init_tech_templates()
    
    def _init_tech_templates(self):
        """Inicializa plantillas de tecnologías base"""
        templates = {
            # WEAPON
            "plasma_rifle": Technology(
                name="Plasma Rifle",
                description="Rifle de plasma avanzado",
                research_type=ResearchType.WEAPON,
                tier=ResearchTier.TIER2,
                required_resources={"credits": 2000, "materials": 100},
                required_time_hours=24.0,
                stat_bonus={"attack": 20}
            ),
            "quantum_blade": Technology(
                name="Quantum Blade",
                description="Espada cuántica",
                research_type=ResearchType.WEAPON,
                tier=ResearchTier.TIER4,
                required_resources={"credits": 10000, "materials": 500},
                required_time_hours=72.0,
                prerequisites=["plasma_rifle"],
                stat_bonus={"attack": 50}
            ),
            # ARMOR
            "titanium_plating": Technology(
                name="Titanium Plating",
                description="Blindaje de titanio",
                research_type=ResearchType.ARMOR,
                tier=ResearchTier.TIER1,
                required_resources={"credits": 1000, "materials": 50},
                required_time_hours=12.0,
                stat_bonus={"defense": 15}
            ),
            # ENGINE
            "hyperdrive": Technology(
                name="Hyperdrive Engine",
                description="Motor hipersónico",
                research_type=ResearchType.ENGINE,
                tier=ResearchTier.TIER3,
                required_resources={"credits": 5000, "materials": 250},
                required_time_hours=48.0,
                stat_bonus={"speed": 30}
            ),
            # AI
            "neural_optimizer": Technology(
                name="Neural Optimizer",
                description="Optimizador de red neuronal",
                research_type=ResearchType.AI,
                tier=ResearchTier.TIER3,
                required_resources={"credits": 4000, "materials": 200},
                required_time_hours=36.0,
                stat_bonus={"intelligence": 25}
            ),
        }
        
        for tech_id, tech in templates.items():
            tech.tech_id = tech_id
            self.technologies[tech_id] = tech
    
    def create_lab(self, name: str, location: str, research_type: ResearchType) -> ResearchLab:
        """Crea nuevo laboratorio"""
        lab = ResearchLab(
            name=name,
            location=location,
            research_type=research_type
        )
        self.labs[lab.lab_id] = lab
        return lab
    
    def get_lab(self, lab_id: str) -> Optional[ResearchLab]:
        """Obtiene laboratorio"""
        return self.labs.get(lab_id)
    
    def start_research(self, lab_id: str, tech_id: str) -> Tuple[bool, str]:
        """Inicia investigación en laboratorio"""
        lab = self.get_lab(lab_id)
        tech = self.technologies.get(tech_id)
        
        if not lab:
            return False, "Lab not found"
        if not tech:
            return False, "Technology not found"
        if not lab.can_start_project():
            return False, "Lab at capacity"
        if lab.credits < tech.required_resources.get("credits", 0):
            return False, "Insufficient credits"
        if lab.materials < tech.required_resources.get("materials", 0):
            return False, "Insufficient materials"
        
        # Verificar prerequisitos
        for prereq in tech.prerequisites:
            if prereq not in lab.completed_projects:
                return False, f"Missing prerequisite: {prereq}"
        
        # Iniciar investigación
        lab.active_projects.append(tech_id)
        lab.credits -= tech.required_resources.get("credits", 0)
        lab.materials -= tech.required_resources.get("materials", 0)
        
        # Clonar technology para tracking de progreso
        tech_copy = Technology(**{k: v for k, v in tech.__dict__.items()})
        tech_copy.progress_percent = 0.0
        self.technologies[tech_id] = tech_copy
        
        return True, f"Research started: {tech.name}"
    
    def update_research_progress(self, time_delta_seconds: float = 3600.0):
        """Actualiza progreso de investigaciones"""
        for lab_id, lab in self.labs.items():
            for tech_id in lab.active_projects[:]:
                tech = self.technologies.get(tech_id)
                if not tech:
                    continue
                
                # Progreso = (delta_tiempo / tiempo_requerido) * bonus
                hours_delta = time_delta_seconds / 3600.0
                required_hours = tech.required_time_hours
                progress_delta = (hours_delta / required_hours) * lab.research_speed_bonus
                
                tech.progress_percent = min(100.0, tech.progress_percent + progress_delta)
                
                # Completar si llega a 100%
                if tech.progress_percent >= 100.0:
                    self.complete_research(lab_id, tech_id)
    
    def complete_research(self, lab_id: str, tech_id: str) -> bool:
        """Completa una investigación"""
        lab = self.get_lab(lab_id)
        tech = self.technologies.get(tech_id)
        
        if not lab or not tech:
            return False
        
        if tech_id in lab.active_projects:
            lab.active_projects.remove(tech_id)
        
        lab.completed_projects.append(tech_id)
        tech.completed = True
        tech.completed_at = datetime.now()
        
        return True
    
    def get_all_labs(self) -> List[ResearchLab]:
        """Obtiene todos los laboratorios"""
        return list(self.labs.values())
    
    def get_labs_by_type(self, research_type: ResearchType) -> List[ResearchLab]:
        """Obtiene labs por tipo"""
        return [lab for lab in self.labs.values() if lab.research_type == research_type]
    
    def get_lab_stats(self) -> Dict:
        """Obtiene estadísticas de investigación"""
        total_completed = sum(len(lab.completed_projects) for lab in self.labs.values())
        total_active = sum(len(lab.active_projects) for lab in self.labs.values())
        
        return {
            "total_labs": len(self.labs),
            "active_projects": total_active,
            "completed_projects": total_completed,
            "technologies_available": len(self.technologies),
            "by_type": {
                rt.value: len(self.get_labs_by_type(rt))
                for rt in ResearchType
            }
        }
    
    def get_research_progress(self, lab_id: str) -> Dict:
        """Obtiene progreso de investigación de un lab"""
        lab = self.get_lab(lab_id)
        if not lab:
            return {}
        
        projects = []
        for tech_id in lab.active_projects:
            tech = self.technologies.get(tech_id)
            if tech:
                projects.append({
                    "tech_id": tech_id,
                    "name": tech.name,
                    "progress": tech.progress_percent,
                    "time_remaining_hours": (100 - tech.progress_percent) / 100 * tech.required_time_hours
                })
        
        return {
            "lab_id": lab_id,
            "lab_name": lab.name,
            "active_projects": projects,
            "capacity": f"{len(lab.active_projects)}/{lab.capacity}"
        }
    
    def upgrade_lab(self, lab_id: str, credits: int) -> bool:
        """Mejora un laboratorio"""
        lab = self.get_lab(lab_id)
        if not lab or credits < 5000:
            return False
        
        lab.level += 1
        lab.capacity += 1
        lab.research_speed_bonus *= 1.1
        
        return True


# Instancia global
research_manager = ResearchManager()
