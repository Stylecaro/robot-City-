"""
Sistema de Economía de Trabajo - Ciudad Robot Metaverso
Permite a los jugadores trabajar, ganar criptomonedas y comprar propiedades
"""

from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid
import random

class JobType(Enum):
    """Tipos de trabajos disponibles"""
    FACTORY_WORKER = "factory_worker"
    RESEARCHER = "researcher"
    MERCHANT = "merchant"
    MECHANIC = "mechanic"
    SECURITY = "security"
    ENERGY_OPERATOR = "energy_operator"
    CONSTRUCTION = "construction"
    ENTERTAINER = "entertainer"
    MEDICAL_STAFF = "medical_staff"
    DATA_ANALYST = "data_analyst"

class JobDifficulty(Enum):
    """Dificultad del trabajo"""
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4
    MASTER = 5

class PropertyType(Enum):
    """Tipos de propiedades"""
    APARTMENT = "apartment"
    HOUSE = "house"
    PENTHOUSE = "penthouse"
    WORKSHOP = "workshop"
    WAREHOUSE = "warehouse"
    OFFICE = "office"
    LAB = "lab"
    STORE = "store"

class WorkShift:
    """Representa un turno de trabajo"""
    def __init__(self, job_type: JobType, difficulty: JobDifficulty, duration_minutes: int = 30):
        self.shift_id = str(uuid.uuid4())
        self.job_type = job_type
        self.difficulty = difficulty
        self.duration_minutes = duration_minutes
        self.base_reward = self._calculate_base_reward()
        self.experience_reward = difficulty.value * 50
        self.energy_cost = difficulty.value * 10
        
    def _calculate_base_reward(self) -> float:
        """Calcula la recompensa base en ROBOT tokens"""
        base_rates = {
            JobType.FACTORY_WORKER: 5.0,
            JobType.RESEARCHER: 15.0,
            JobType.MERCHANT: 8.0,
            JobType.MECHANIC: 10.0,
            JobType.SECURITY: 7.0,
            JobType.ENERGY_OPERATOR: 12.0,
            JobType.CONSTRUCTION: 9.0,
            JobType.ENTERTAINER: 6.0,
            JobType.MEDICAL_STAFF: 14.0,
            JobType.DATA_ANALYST: 13.0
        }
        return base_rates.get(self.job_type, 5.0) * self.difficulty.value
    
    def to_dict(self) -> Dict:
        return {
            "shift_id": self.shift_id,
            "job_type": self.job_type.value,
            "difficulty": self.difficulty.value,
            "duration_minutes": self.duration_minutes,
            "base_reward": self.base_reward,
            "experience_reward": self.experience_reward,
            "energy_cost": self.energy_cost
        }

class WorkSession:
    """Sesión de trabajo activa"""
    def __init__(self, player_id: str, shift: WorkShift):
        self.session_id = str(uuid.uuid4())
        self.player_id = player_id
        self.shift = shift
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(minutes=shift.duration_minutes)
        self.completed = False
        self.performance_score = 0.0  # 0-100
        self.actual_reward = 0.0
        
    def complete_work(self, performance_score: float) -> Dict:
        """Completa el trabajo y calcula recompensas"""
        self.completed = True
        self.performance_score = min(100.0, max(0.0, performance_score))
        
        # Multiplicador de rendimiento (0.5x - 2.0x)
        performance_multiplier = 0.5 + (self.performance_score / 100.0) * 1.5
        self.actual_reward = self.shift.base_reward * performance_multiplier
        
        return {
            "session_id": self.session_id,
            "completed": True,
            "performance_score": self.performance_score,
            "tokens_earned": round(self.actual_reward, 2),
            "experience_earned": int(self.shift.experience_reward * performance_multiplier),
            "completion_time": datetime.now().isoformat()
        }
    
    def to_dict(self) -> Dict:
        return {
            "session_id": self.session_id,
            "player_id": self.player_id,
            "shift": self.shift.to_dict(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "completed": self.completed,
            "performance_score": self.performance_score,
            "actual_reward": self.actual_reward
        }

class Property:
    """Propiedad que puede ser comprada/alquilada"""
    def __init__(self, property_type: PropertyType, location: str, zone_id: str):
        self.property_id = str(uuid.uuid4())
        self.property_type = property_type
        self.location = location
        self.zone_id = zone_id
        self.owner_id: Optional[str] = None
        self.purchase_price = self._calculate_price()
        self.monthly_cost = self.purchase_price * 0.05  # 5% mensual
        self.size_sqm = self._calculate_size()
        self.level = 1
        self.amenities: List[str] = []
        self.passive_income = 0.0  # Tokens por día si se alquila
        
    def _calculate_price(self) -> float:
        """Calcula precio en ROBOT tokens"""
        base_prices = {
            PropertyType.APARTMENT: 1000.0,
            PropertyType.HOUSE: 2500.0,
            PropertyType.PENTHOUSE: 10000.0,
            PropertyType.WORKSHOP: 3000.0,
            PropertyType.WAREHOUSE: 5000.0,
            PropertyType.OFFICE: 4000.0,
            PropertyType.LAB: 8000.0,
            PropertyType.STORE: 3500.0
        }
        return base_prices.get(self.property_type, 1000.0)
    
    def _calculate_size(self) -> int:
        """Calcula tamaño en metros cuadrados"""
        sizes = {
            PropertyType.APARTMENT: 60,
            PropertyType.HOUSE: 120,
            PropertyType.PENTHOUSE: 250,
            PropertyType.WORKSHOP: 100,
            PropertyType.WAREHOUSE: 500,
            PropertyType.OFFICE: 80,
            PropertyType.LAB: 150,
            PropertyType.STORE: 90
        }
        return sizes.get(self.property_type, 50)
    
    def purchase(self, player_id: str) -> bool:
        """Compra la propiedad"""
        if self.owner_id is None:
            self.owner_id = player_id
            return True
        return False
    
    def upgrade(self) -> Dict:
        """Mejora la propiedad"""
        upgrade_cost = self.purchase_price * 0.3 * self.level
        self.level += 1
        self.passive_income = self.purchase_price * 0.01 * self.level  # 1% por nivel
        
        return {
            "property_id": self.property_id,
            "new_level": self.level,
            "upgrade_cost": upgrade_cost,
            "new_passive_income": self.passive_income
        }
    
    def to_dict(self) -> Dict:
        return {
            "property_id": self.property_id,
            "property_type": self.property_type.value,
            "location": self.location,
            "zone_id": self.zone_id,
            "owner_id": self.owner_id,
            "purchase_price": self.purchase_price,
            "monthly_cost": self.monthly_cost,
            "size_sqm": self.size_sqm,
            "level": self.level,
            "amenities": self.amenities,
            "passive_income": self.passive_income,
            "is_available": self.owner_id is None
        }

class PlayerEconomy:
    """Economía personal del jugador"""
    def __init__(self, player_id: str):
        self.player_id = player_id
        self.wallet_balance = 100.0  # Tokens ROBOT iniciales
        self.total_earned = 100.0
        self.total_spent = 0.0
        self.energy = 100  # 0-100
        self.work_experience = 0
        self.work_level = 1
        self.owned_properties: List[str] = []
        self.active_work_session: Optional[WorkSession] = None
        self.work_history: List[Dict] = []
        
    def can_work(self) -> bool:
        """Verifica si el jugador puede trabajar"""
        return (self.energy >= 10 and 
                self.active_work_session is None)
    
    def start_work(self, shift: WorkShift) -> Dict:
        """Inicia una sesión de trabajo"""
        if not self.can_work():
            return {"error": "No puedes trabajar ahora (energía baja o ya estás trabajando)"}
        
        if self.energy < shift.energy_cost:
            return {"error": f"Energía insuficiente. Necesitas {shift.energy_cost}, tienes {self.energy}"}
        
        self.active_work_session = WorkSession(self.player_id, shift)
        self.energy -= shift.energy_cost
        
        return {
            "success": True,
            "session": self.active_work_session.to_dict(),
            "remaining_energy": self.energy
        }
    
    def complete_work(self, performance_score: float = 75.0) -> Dict:
        """Completa el trabajo actual"""
        if self.active_work_session is None:
            return {"error": "No hay sesión de trabajo activa"}
        
        result = self.active_work_session.complete_work(performance_score)
        
        # Actualizar economía
        self.wallet_balance += result["tokens_earned"]
        self.total_earned += result["tokens_earned"]
        self.work_experience += result["experience_earned"]
        
        # Subir de nivel cada 1000 XP
        new_level = 1 + (self.work_experience // 1000)
        if new_level > self.work_level:
            self.work_level = new_level
            result["level_up"] = True
            result["new_level"] = self.work_level
        
        # Guardar en historial
        self.work_history.append({
            "session_id": result["session_id"],
            "timestamp": result["completion_time"],
            "earned": result["tokens_earned"]
        })
        
        self.active_work_session = None
        
        return result
    
    def purchase_property(self, property_obj: Property) -> Dict:
        """Compra una propiedad"""
        if property_obj.owner_id is not None:
            return {"error": "Propiedad ya tiene dueño"}
        
        if self.wallet_balance < property_obj.purchase_price:
            return {
                "error": "Fondos insuficientes",
                "required": property_obj.purchase_price,
                "available": self.wallet_balance
            }
        
        # Realizar compra
        self.wallet_balance -= property_obj.purchase_price
        self.total_spent += property_obj.purchase_price
        property_obj.purchase(self.player_id)
        self.owned_properties.append(property_obj.property_id)
        
        return {
            "success": True,
            "property": property_obj.to_dict(),
            "new_balance": self.wallet_balance,
            "total_properties": len(self.owned_properties)
        }
    
    def regenerate_energy(self, amount: int = 20):
        """Regenera energía (puede ser por descanso, consumibles, etc)"""
        self.energy = min(100, self.energy + amount)
    
    def collect_passive_income(self, properties: List[Property]) -> float:
        """Recolecta ingreso pasivo de propiedades"""
        daily_income = sum(p.passive_income for p in properties if p.owner_id == self.player_id)
        self.wallet_balance += daily_income
        self.total_earned += daily_income
        return daily_income
    
    def to_dict(self) -> Dict:
        return {
            "player_id": self.player_id,
            "wallet_balance": round(self.wallet_balance, 2),
            "total_earned": round(self.total_earned, 2),
            "total_spent": round(self.total_spent, 2),
            "energy": self.energy,
            "work_experience": self.work_experience,
            "work_level": self.work_level,
            "owned_properties": self.owned_properties,
            "is_working": self.active_work_session is not None,
            "work_history_count": len(self.work_history)
        }

class EconomyManager:
    """Gestor central de economía de trabajo"""
    def __init__(self):
        self.players: Dict[str, PlayerEconomy] = {}
        self.properties: Dict[str, Property] = {}
        self.available_jobs: Dict[str, List[WorkShift]] = {}
        self._initialize_properties()
        self._initialize_jobs()
    
    def _initialize_properties(self):
        """Crea propiedades iniciales en las zonas"""
        zones = [
            ("Industrial District", "zone_industrial"),
            ("Commercial Hub", "zone_commercial"),
            ("Residential Sector", "zone_residential"),
            ("Research Labs", "zone_research"),
            ("Entertainment Zone", "zone_entertainment")
        ]
        
        for zone_name, zone_id in zones:
            # 5 propiedades por zona
            for i in range(5):
                if "Residential" in zone_name:
                    prop_types = [PropertyType.APARTMENT, PropertyType.HOUSE, PropertyType.PENTHOUSE]
                elif "Commercial" in zone_name:
                    prop_types = [PropertyType.STORE, PropertyType.OFFICE]
                elif "Industrial" in zone_name:
                    prop_types = [PropertyType.WORKSHOP, PropertyType.WAREHOUSE]
                elif "Research" in zone_name:
                    prop_types = [PropertyType.LAB, PropertyType.OFFICE]
                else:
                    prop_types = [PropertyType.APARTMENT, PropertyType.STORE]
                
                prop_type = random.choice(prop_types)
                prop = Property(prop_type, f"{zone_name} #{i+1}", zone_id)
                self.properties[prop.property_id] = prop
    
    def _initialize_jobs(self):
        """Crea trabajos disponibles por zona"""
        job_zones = {
            "zone_industrial": [JobType.FACTORY_WORKER, JobType.MECHANIC, JobType.CONSTRUCTION],
            "zone_commercial": [JobType.MERCHANT, JobType.SECURITY, JobType.DATA_ANALYST],
            "zone_research": [JobType.RESEARCHER, JobType.MEDICAL_STAFF, JobType.DATA_ANALYST],
            "zone_entertainment": [JobType.ENTERTAINER, JobType.SECURITY],
            "zone_energy": [JobType.ENERGY_OPERATOR, JobType.MECHANIC]
        }
        
        for zone_id, job_types in job_zones.items():
            self.available_jobs[zone_id] = []
            for job_type in job_types:
                for difficulty in [JobDifficulty.EASY, JobDifficulty.MEDIUM, JobDifficulty.HARD]:
                    shift = WorkShift(job_type, difficulty, duration_minutes=30)
                    self.available_jobs[zone_id].append(shift)
    
    def get_player(self, player_id: str) -> PlayerEconomy:
        """Obtiene o crea jugador"""
        if player_id not in self.players:
            self.players[player_id] = PlayerEconomy(player_id)
        return self.players[player_id]
    
    def get_available_jobs(self, zone_id: Optional[str] = None) -> List[Dict]:
        """Lista trabajos disponibles"""
        if zone_id:
            return [shift.to_dict() for shift in self.available_jobs.get(zone_id, [])]
        
        all_jobs = []
        for zone_jobs in self.available_jobs.values():
            all_jobs.extend([shift.to_dict() for shift in zone_jobs])
        return all_jobs
    
    def get_available_properties(self, zone_id: Optional[str] = None, 
                                 property_type: Optional[PropertyType] = None) -> List[Dict]:
        """Lista propiedades disponibles para compra"""
        properties = [
            p.to_dict() for p in self.properties.values()
            if p.owner_id is None
        ]
        
        if zone_id:
            properties = [p for p in properties if p["zone_id"] == zone_id]
        
        if property_type:
            properties = [p for p in properties if p["property_type"] == property_type.value]
        
        return properties
    
    def get_player_properties(self, player_id: str) -> List[Dict]:
        """Obtiene propiedades del jugador"""
        return [
            p.to_dict() for p in self.properties.values()
            if p.owner_id == player_id
        ]
    
    def start_work_shift(self, player_id: str, shift_id: str) -> Dict:
        """Inicia turno de trabajo"""
        player = self.get_player(player_id)
        
        # Buscar el shift
        shift = None
        for zone_jobs in self.available_jobs.values():
            for s in zone_jobs:
                if s.shift_id == shift_id:
                    shift = s
                    break
            if shift:
                break
        
        if not shift:
            return {"error": "Trabajo no encontrado"}
        
        return player.start_work(shift)
    
    def get_economy_stats(self) -> Dict:
        """Estadísticas globales de economía"""
        total_players = len(self.players)
        total_tokens_circulation = sum(p.wallet_balance for p in self.players.values())
        total_properties_sold = len([p for p in self.properties.values() if p.owner_id])
        total_work_sessions = sum(len(p.work_history) for p in self.players.values())
        
        return {
            "total_players": total_players,
            "tokens_in_circulation": round(total_tokens_circulation, 2),
            "properties_available": len(self.properties) - total_properties_sold,
            "properties_sold": total_properties_sold,
            "total_work_sessions": total_work_sessions,
            "average_player_balance": round(total_tokens_circulation / max(1, total_players), 2)
        }

# Instancia global
economy_manager = EconomyManager()
