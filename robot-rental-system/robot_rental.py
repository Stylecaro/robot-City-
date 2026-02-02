"""
Sistema de Renta de Robots Asistentes - Ciudad Robot Metaverso
Permite crear y rentar robots asistentes para diferentes tareas
"""

from enum import Enum
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import uuid
import random

class AssistantType(Enum):
    """Tipos de robots asistentes"""
    PERSONAL = "personal"          # Asistente personal general
    CORPORATE = "corporate"        # Para empresas
    MEDICAL = "medical"            # Asistente médico
    RESEARCH = "research"          # Investigación
    SECURITY = "security"          # Seguridad
    LOGISTICS = "logistics"        # Logística
    ENTERTAINMENT = "entertainment" # Entretenimiento
    EDUCATION = "education"        # Educación

class TaskType(Enum):
    """Tipos de tareas que pueden realizar"""
    DATA_ANALYSIS = "data_analysis"
    CUSTOMER_SERVICE = "customer_service"
    SCHEDULING = "scheduling"
    DOCUMENT_MANAGEMENT = "document_management"
    MONITORING = "monitoring"
    CONTENT_CREATION = "content_creation"
    TUTORING = "tutoring"
    HEALTH_TRACKING = "health_tracking"
    ENTERTAINMENT = "entertainment"
    RESEARCH_SUPPORT = "research_support"

class RentalPeriod(Enum):
    """Período de renta"""
    HOURLY = "hourly"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class AssistantBot:
    """Robot asistente rentable"""
    def __init__(self, owner_id: str, assistant_type: AssistantType, name: str = ""):
        self.bot_id = str(uuid.uuid4())
        self.owner_id = owner_id
        self.assistant_type = assistant_type
        self.name = name or f"Assistant_{assistant_type.value}_{self.bot_id[:4]}"
        self.version = "1.0"
        self.creation_date = datetime.now()
        self.performance_score = 75  # 0-100
        self.reliability = 95  # 0-100
        self.tasks_completed = 0
        self.tasks_failed = 0
        self.total_usage_hours = 0
        self.capabilities: List[TaskType] = self._get_base_capabilities()
        self.rental_price_hourly = self._calculate_rental_price()
        self.custom_settings: Dict = {}
        self.is_rented = False
        self.current_renter_id: Optional[str] = None
        self.rental_history: List[Dict] = []
        
    def _get_base_capabilities(self) -> List[TaskType]:
        """Obtiene capacidades base según tipo"""
        capabilities_map = {
            AssistantType.PERSONAL: [
                TaskType.SCHEDULING, TaskType.DOCUMENT_MANAGEMENT,
                TaskType.CUSTOMER_SERVICE, TaskType.ENTERTAINMENT
            ],
            AssistantType.CORPORATE: [
                TaskType.DATA_ANALYSIS, TaskType.CUSTOMER_SERVICE,
                TaskType.SCHEDULING, TaskType.MONITORING
            ],
            AssistantType.MEDICAL: [
                TaskType.HEALTH_TRACKING, TaskType.MONITORING,
                TaskType.DATA_ANALYSIS, TaskType.RESEARCH_SUPPORT
            ],
            AssistantType.RESEARCH: [
                TaskType.DATA_ANALYSIS, TaskType.RESEARCH_SUPPORT,
                TaskType.DOCUMENT_MANAGEMENT, TaskType.CONTENT_CREATION
            ],
            AssistantType.SECURITY: [
                TaskType.MONITORING, TaskType.DATA_ANALYSIS,
                TaskType.CUSTOMER_SERVICE
            ],
            AssistantType.LOGISTICS: [
                TaskType.SCHEDULING, TaskType.MONITORING,
                TaskType.DATA_ANALYSIS, TaskType.DOCUMENT_MANAGEMENT
            ],
            AssistantType.ENTERTAINMENT: [
                TaskType.ENTERTAINMENT, TaskType.CONTENT_CREATION,
                TaskType.CUSTOMER_SERVICE, TaskType.SCHEDULING
            ],
            AssistantType.EDUCATION: [
                TaskType.TUTORING, TaskType.CONTENT_CREATION,
                TaskType.SCHEDULING, TaskType.DOCUMENT_MANAGEMENT
            ]
        }
        return capabilities_map.get(self.assistant_type, [TaskType.CUSTOMER_SERVICE])
    
    def _calculate_rental_price(self) -> float:
        """Calcula precio de renta por hora en ROBOT tokens"""
        base_prices = {
            AssistantType.PERSONAL: 2.0,
            AssistantType.CORPORATE: 5.0,
            AssistantType.MEDICAL: 10.0,
            AssistantType.RESEARCH: 8.0,
            AssistantType.SECURITY: 6.0,
            AssistantType.LOGISTICS: 4.5,
            AssistantType.ENTERTAINMENT: 3.0,
            AssistantType.EDUCATION: 7.0
        }
        return base_prices.get(self.assistant_type, 2.0)
    
    def execute_task(self, task_type: TaskType, complexity: int = 1) -> Dict:
        """Ejecuta una tarea"""
        if task_type not in self.capabilities:
            return {"success": False, "error": f"Capacidad {task_type.value} no disponible"}
        
        # Calcular éxito basado en reliability
        success_chance = self.reliability - (complexity * 5)
        success = random.randint(1, 100) <= success_chance
        
        if success:
            self.tasks_completed += 1
            performance_gain = random.randint(1, 5)
            self.performance_score = min(100, self.performance_score + performance_gain)
            
            result = {
                "success": True,
                "task_result": self._generate_task_result(task_type),
                "completion_time": f"{random.randint(5, 60)} minutes",
                "quality_score": random.randint(80, 100)
            }
        else:
            self.tasks_failed += 1
            result = {
                "success": False,
                "error": "Tarea completada con errores",
                "partial_result": self._generate_task_result(task_type, partial=True)
            }
        
        return result
    
    def _generate_task_result(self, task_type: TaskType, partial: bool = False) -> str:
        """Genera resultado de tarea"""
        results = {
            TaskType.DATA_ANALYSIS: f"Analysis Report - Confidence: {random.randint(70, 100)}%",
            TaskType.CUSTOMER_SERVICE: "Customer inquiry resolved",
            TaskType.SCHEDULING: "Schedule updated successfully",
            TaskType.DOCUMENT_MANAGEMENT: "Documents organized and tagged",
            TaskType.MONITORING: "System status: Optimal",
            TaskType.CONTENT_CREATION: "Content generated: 5000 words",
            TaskType.TUTORING: "Lesson completed - Student progress: 85%",
            TaskType.HEALTH_TRACKING: "Health metrics recorded and analyzed",
            TaskType.ENTERTAINMENT: "Entertainment event scheduled",
            TaskType.RESEARCH_SUPPORT: "Research data compiled and categorized"
        }
        
        result = results.get(task_type, "Task completed")
        if partial:
            result += " (Partial)"
        return result
    
    def upgrade_capability(self, task_type: TaskType) -> Dict:
        """Mejora una capacidad del bot"""
        if task_type in self.capabilities:
            return {"error": "Ya posee esta capacidad"}
        
        upgrade_cost = 1000  # ROBOT tokens
        self.capabilities.append(task_type)
        
        return {
            "success": True,
            "new_capability": task_type.value,
            "cost": upgrade_cost,
            "total_capabilities": len(self.capabilities)
        }
    
    def rent_out(self, renter_id: str, period: RentalPeriod) -> Dict:
        """Renta el bot a otro jugador"""
        if self.is_rented:
            return {"error": "Bot ya está rentado"}
        
        self.is_rented = True
        self.current_renter_id = renter_id
        rental_start = datetime.now()
        
        period_durations = {
            RentalPeriod.HOURLY: timedelta(hours=1),
            RentalPeriod.DAILY: timedelta(days=1),
            RentalPeriod.WEEKLY: timedelta(weeks=1),
            RentalPeriod.MONTHLY: timedelta(days=30)
        }
        
        rental_end = rental_start + period_durations.get(period, timedelta(days=1))
        
        rental_record = {
            "renter_id": renter_id,
            "period": period.value,
            "start": rental_start.isoformat(),
            "end": rental_end.isoformat(),
            "rental_cost": self._calculate_rental_cost(period)
        }
        
        self.rental_history.append(rental_record)
        
        return {
            "success": True,
            "rental": rental_record,
            "bot_id": self.bot_id,
            "bot_name": self.name
        }
    
    def _calculate_rental_cost(self, period: RentalPeriod) -> float:
        """Calcula costo de renta"""
        multipliers = {
            RentalPeriod.HOURLY: 1,
            RentalPeriod.DAILY: 20,
            RentalPeriod.WEEKLY: 120,
            RentalPeriod.MONTHLY: 400
        }
        
        return self.rental_price_hourly * multipliers.get(period, 1)
    
    def return_from_rental(self) -> bool:
        """Devuelve el bot de renta"""
        if not self.is_rented:
            return False
        
        self.is_rented = False
        self.current_renter_id = None
        return True
    
    def to_dict(self) -> Dict:
        return {
            "bot_id": self.bot_id,
            "owner_id": self.owner_id,
            "name": self.name,
            "type": self.assistant_type.value,
            "version": self.version,
            "creation_date": self.creation_date.isoformat(),
            "performance_score": self.performance_score,
            "reliability": self.reliability,
            "tasks_completed": self.tasks_completed,
            "tasks_failed": self.tasks_failed,
            "total_usage_hours": self.total_usage_hours,
            "capabilities": [c.value for c in self.capabilities],
            "rental_price_hourly": self.rental_price_hourly,
            "is_rented": self.is_rented,
            "current_renter_id": self.current_renter_id,
            "rentals_count": len(self.rental_history)
        }

class RentalManager:
    """Gestor de rentas de bots"""
    def __init__(self):
        self.bots: Dict[str, AssistantBot] = {}
        self.active_rentals: Dict[str, Dict] = {}  # renter_id -> rental_info
        self.total_rental_revenue = 0.0
        
    def create_bot(self, owner_id: str, assistant_type: AssistantType, name: str = "") -> AssistantBot:
        """Crea nuevo bot asistente"""
        bot = AssistantBot(owner_id, assistant_type, name)
        self.bots[bot.bot_id] = bot
        return bot
    
    def get_bot(self, bot_id: str) -> Optional[AssistantBot]:
        """Obtiene bot por ID"""
        return self.bots.get(bot_id)
    
    def get_owner_bots(self, owner_id: str) -> List[AssistantBot]:
        """Obtiene bots de un propietario"""
        return [b for b in self.bots.values() if b.owner_id == owner_id]
    
    def get_available_bots(self, assistant_type: Optional[AssistantType] = None) -> List[AssistantBot]:
        """Obtiene bots disponibles para rentar"""
        bots = [b for b in self.bots.values() if not b.is_rented]
        
        if assistant_type:
            bots = [b for b in bots if b.assistant_type == assistant_type]
        
        return sorted(bots, key=lambda b: b.performance_score, reverse=True)
    
    def rent_bot(self, bot_id: str, renter_id: str, period: RentalPeriod) -> Dict:
        """Renta un bot"""
        bot = self.get_bot(bot_id)
        
        if not bot:
            return {"error": "Bot no encontrado"}
        
        if bot.is_rented:
            return {"error": "Bot ya está rentado"}
        
        rental_cost = bot._calculate_rental_cost(period)
        rental_result = bot.rent_out(renter_id, period)
        
        if rental_result.get("success"):
            self.active_rentals[renter_id] = {
                "bot_id": bot_id,
                "rental_cost": rental_cost,
                "rental_info": rental_result["rental"]
            }
            self.total_rental_revenue += rental_cost
        
        return rental_result
    
    def return_bot(self, renter_id: str) -> Dict:
        """Devuelve bot rentado"""
        if renter_id not in self.active_rentals:
            return {"error": "No tienes bots rentados"}
        
        rental_info = self.active_rentals[renter_id]
        bot = self.get_bot(rental_info["bot_id"])
        
        if bot and bot.return_from_rental():
            del self.active_rentals[renter_id]
            return {"success": True, "message": "Bot devuelto"}
        
        return {"error": "Error al devolver bot"}
    
    def get_rental_marketplace(self) -> List[Dict]:
        """Marketplace de bots para rentar"""
        available = self.get_available_bots()
        return [
            {
                "bot_id": b.bot_id,
                "name": b.name,
                "type": b.assistant_type.value,
                "performance": b.performance_score,
                "reliability": b.reliability,
                "tasks_completed": b.tasks_completed,
                "hourly_price": b.rental_price_hourly,
                "capabilities": [c.value for c in b.capabilities],
                "owner_id": b.owner_id
            }
            for b in available
        ]

# Instancia global
rental_manager = RentalManager()
