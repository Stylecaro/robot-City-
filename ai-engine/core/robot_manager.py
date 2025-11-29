"""
Gestor de Robots - Sistema de gestión y coordinación de robots virtuales
Maneja la creación, control y monitoreo de todos los robots en la ciudad
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import logging
import random
import json

logger = logging.getLogger("robot_manager")

class RobotType(Enum):
    """Tipos de robots disponibles"""
    CONSTRUCTION = "construction"
    MAINTENANCE = "maintenance"
    SECURITY = "security"
    TRANSPORT = "transport"
    CLEANING = "cleaning"
    ANALYSIS = "analysis"
    COMMUNICATION = "communication"
    EMERGENCY = "emergency"

class RobotStatus(Enum):
    """Estados de los robots"""
    ACTIVE = "active"
    IDLE = "idle"
    MAINTENANCE = "maintenance"
    CHARGING = "charging"
    ERROR = "error"
    OFFLINE = "offline"

@dataclass
class Position:
    """Posición 3D del robot"""
    x: float
    y: float
    z: float

@dataclass
class RobotCapabilities:
    """Capacidades del robot"""
    strength: float  # 0.0 - 1.0
    speed: float
    intelligence: float
    energy_efficiency: float
    communication_range: float
    payload_capacity: float
    precision: float
    durability: float

@dataclass
class RobotStats:
    """Estadísticas del robot"""
    tasks_completed: int
    uptime_hours: float
    energy_consumed: float
    distance_traveled: float
    efficiency_rating: float
    last_maintenance: str
    errors_count: int

class VirtualRobot:
    """Clase base para robots virtuales"""
    
    def __init__(self, robot_type: RobotType, config: Dict[str, Any]):
        self.id = str(uuid.uuid4())
        self.name = config.get("name", f"Robot-{self.id[:8]}")
        self.type = robot_type
        self.status = RobotStatus.ACTIVE
        self.position = Position(
            x=config.get("x", 0.0),
            y=config.get("y", 0.0),
            z=config.get("z", 0.0)
        )
        
        # Capacidades basadas en el tipo
        self.capabilities = self._generate_capabilities(robot_type, config)
        
        # Estado del robot
        self.energy_level = 100.0
        self.current_task = None
        self.task_queue = []
        self.creation_time = datetime.now()
        
        # Estadísticas
        self.stats = RobotStats(
            tasks_completed=0,
            uptime_hours=0.0,
            energy_consumed=0.0,
            distance_traveled=0.0,
            efficiency_rating=1.0,
            last_maintenance=datetime.now().isoformat(),
            errors_count=0
        )
        
        # Estado interno
        self.learning_data = {}
        self.memory_bank = []
        
        logger.info(f"Robot {self.name} ({self.type.value}) creado")
    
    def _generate_capabilities(self, robot_type: RobotType, config: Dict) -> RobotCapabilities:
        """Generar capacidades basadas en el tipo de robot"""
        base_capabilities = {
            RobotType.CONSTRUCTION: {
                "strength": 0.9, "speed": 0.6, "intelligence": 0.7,
                "energy_efficiency": 0.5, "communication_range": 0.8,
                "payload_capacity": 0.9, "precision": 0.8, "durability": 0.9
            },
            RobotType.MAINTENANCE: {
                "strength": 0.7, "speed": 0.8, "intelligence": 0.9,
                "energy_efficiency": 0.8, "communication_range": 0.7,
                "payload_capacity": 0.6, "precision": 0.95, "durability": 0.8
            },
            RobotType.SECURITY: {
                "strength": 0.8, "speed": 0.9, "intelligence": 0.8,
                "energy_efficiency": 0.7, "communication_range": 0.9,
                "payload_capacity": 0.5, "precision": 0.9, "durability": 0.9
            },
            RobotType.TRANSPORT: {
                "strength": 0.6, "speed": 0.95, "intelligence": 0.6,
                "energy_efficiency": 0.9, "communication_range": 0.8,
                "payload_capacity": 0.95, "precision": 0.7, "durability": 0.8
            },
            RobotType.CLEANING: {
                "strength": 0.5, "speed": 0.7, "intelligence": 0.6,
                "energy_efficiency": 0.9, "communication_range": 0.6,
                "payload_capacity": 0.7, "precision": 0.8, "durability": 0.7
            },
            RobotType.ANALYSIS: {
                "strength": 0.3, "speed": 0.5, "intelligence": 0.95,
                "energy_efficiency": 0.95, "communication_range": 0.95,
                "payload_capacity": 0.3, "precision": 0.95, "durability": 0.6
            },
            RobotType.COMMUNICATION: {
                "strength": 0.3, "speed": 0.8, "intelligence": 0.9,
                "energy_efficiency": 0.8, "communication_range": 0.99,
                "payload_capacity": 0.4, "precision": 0.8, "durability": 0.7
            },
            RobotType.EMERGENCY: {
                "strength": 0.8, "speed": 0.95, "intelligence": 0.9,
                "energy_efficiency": 0.6, "communication_range": 0.9,
                "payload_capacity": 0.8, "precision": 0.9, "durability": 0.95
            }
        }
        
        caps = base_capabilities.get(robot_type, base_capabilities[RobotType.MAINTENANCE])
        
        # Aplicar variaciones aleatorias y configuración personalizada
        for key, base_value in caps.items():
            variation = random.uniform(-0.1, 0.1)
            custom_value = config.get(key, base_value + variation)
            caps[key] = max(0.0, min(1.0, custom_value))
        
        return RobotCapabilities(**caps)
    
    async def update(self):
        """Actualizar estado del robot"""
        # Consumir energía basado en actividad
        energy_consumption = self._calculate_energy_consumption()
        self.energy_level = max(0.0, self.energy_level - energy_consumption)
        
        # Actualizar estadísticas
        self.stats.uptime_hours += 1/3600  # Asumiendo updates cada segundo
        self.stats.energy_consumed += energy_consumption
        
        # Verificar si necesita carga
        if self.energy_level < 20.0 and self.status != RobotStatus.CHARGING:
            await self.start_charging()
        elif self.energy_level > 90.0 and self.status == RobotStatus.CHARGING:
            await self.stop_charging()
        
        # Procesar tareas pendientes
        if self.current_task is None and self.task_queue:
            await self.start_next_task()
        
        # Procesar tarea actual
        if self.current_task:
            await self.process_current_task()
    
    def _calculate_energy_consumption(self) -> float:
        """Calcular consumo de energía basado en estado y actividad"""
        base_consumption = 0.1  # Consumo base por segundo
        
        if self.status == RobotStatus.ACTIVE:
            # Consumo mayor cuando está activo
            activity_factor = 1.0 - self.capabilities.energy_efficiency
            return base_consumption * (1.0 + activity_factor)
        elif self.status == RobotStatus.IDLE:
            return base_consumption * 0.3
        elif self.status == RobotStatus.CHARGING:
            return -2.0  # Recupera energía
        else:
            return base_consumption * 0.5
    
    async def start_charging(self):
        """Iniciar proceso de carga"""
        self.status = RobotStatus.CHARGING
        logger.info(f"Robot {self.name} iniciando carga (energía: {self.energy_level:.1f}%)")
    
    async def stop_charging(self):
        """Detener proceso de carga"""
        self.status = RobotStatus.ACTIVE
        logger.info(f"Robot {self.name} carga completa (energía: {self.energy_level:.1f}%)")
    
    async def add_task(self, task: Dict[str, Any]):
        """Añadir tarea a la cola"""
        task["id"] = str(uuid.uuid4())
        task["created_at"] = datetime.now().isoformat()
        task["status"] = "pending"
        self.task_queue.append(task)
        logger.info(f"Tarea añadida a {self.name}: {task.get('type', 'unknown')}")
    
    async def start_next_task(self):
        """Iniciar la siguiente tarea en la cola"""
        if not self.task_queue:
            return
        
        self.current_task = self.task_queue.pop(0)
        self.current_task["status"] = "in_progress"
        self.current_task["started_at"] = datetime.now().isoformat()
        self.status = RobotStatus.ACTIVE
        
        logger.info(f"Robot {self.name} iniciando tarea: {self.current_task.get('type')}")
    
    async def process_current_task(self):
        """Procesar la tarea actual"""
        if not self.current_task:
            return
        
        task_type = self.current_task.get("type", "unknown")
        duration = self.current_task.get("duration", 5.0)  # Duración en segundos
        
        # Simular progreso de la tarea
        if "progress" not in self.current_task:
            self.current_task["progress"] = 0.0
        
        # Calcular progreso basado en capacidades del robot
        progress_rate = self._calculate_progress_rate(task_type)
        self.current_task["progress"] += progress_rate
        
        # Verificar si la tarea está completa
        if self.current_task["progress"] >= 1.0:
            await self.complete_current_task()
    
    def _calculate_progress_rate(self, task_type: str) -> float:
        """Calcular velocidad de progreso según el tipo de tarea"""
        base_rate = 0.02  # 2% por update (50 segundos para completar)
        
        # Modificar velocidad según capacidades relevantes
        efficiency_factors = {
            "construction": self.capabilities.strength * 0.5 + self.capabilities.precision * 0.5,
            "maintenance": self.capabilities.intelligence * 0.7 + self.capabilities.precision * 0.3,
            "security": self.capabilities.speed * 0.6 + self.capabilities.intelligence * 0.4,
            "transport": self.capabilities.speed * 0.8 + self.capabilities.payload_capacity * 0.2,
            "cleaning": self.capabilities.speed * 0.6 + self.capabilities.precision * 0.4,
            "analysis": self.capabilities.intelligence * 0.9 + self.capabilities.communication_range * 0.1
        }
        
        efficiency = efficiency_factors.get(task_type, 0.7)
        return base_rate * efficiency
    
    async def complete_current_task(self):
        """Completar la tarea actual"""
        if not self.current_task:
            return
        
        self.current_task["status"] = "completed"
        self.current_task["completed_at"] = datetime.now().isoformat()
        
        # Actualizar estadísticas
        self.stats.tasks_completed += 1
        
        # Calcular eficiencia de la tarea
        task_efficiency = min(1.0, self.current_task["progress"])
        self.stats.efficiency_rating = (
            self.stats.efficiency_rating * 0.9 + task_efficiency * 0.1
        )
        
        # Aprender de la tarea completada
        await self.learn_from_task(self.current_task)
        
        # Guardar en memoria
        self.memory_bank.append(self.current_task.copy())
        if len(self.memory_bank) > 100:  # Limitar memoria
            self.memory_bank.pop(0)
        
        logger.info(f"Robot {self.name} completó tarea: {self.current_task.get('type')}")
        
        # Limpiar tarea actual
        self.current_task = None
        self.status = RobotStatus.IDLE if not self.task_queue else RobotStatus.ACTIVE
    
    async def learn_from_task(self, task: Dict):
        """Aprender de la tarea completada para mejorar futuro rendimiento"""
        task_type = task.get("type", "unknown")
        efficiency = task.get("progress", 0.0)
        
        # Actualizar datos de aprendizaje
        if task_type not in self.learning_data:
            self.learning_data[task_type] = {
                "attempts": 0,
                "total_efficiency": 0.0,
                "average_efficiency": 0.0,
                "improvements": 0.0
            }
        
        data = self.learning_data[task_type]
        data["attempts"] += 1
        data["total_efficiency"] += efficiency
        data["average_efficiency"] = data["total_efficiency"] / data["attempts"]
        
        # Pequeña mejora en capacidades relacionadas
        if efficiency > 0.8:  # Tarea exitosa
            improvement = 0.001  # Mejora gradual
            
            if task_type == "construction":
                self.capabilities.strength = min(1.0, self.capabilities.strength + improvement)
                self.capabilities.precision = min(1.0, self.capabilities.precision + improvement)
            elif task_type == "maintenance":
                self.capabilities.intelligence = min(1.0, self.capabilities.intelligence + improvement)
            elif task_type == "security":
                self.capabilities.speed = min(1.0, self.capabilities.speed + improvement)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir robot a diccionario para serialización"""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value,
            "status": self.status.value,
            "position": asdict(self.position),
            "capabilities": asdict(self.capabilities),
            "energy_level": self.energy_level,
            "current_task": self.current_task,
            "task_queue_size": len(self.task_queue),
            "stats": asdict(self.stats),
            "creation_time": self.creation_time.isoformat(),
            "learning_progress": len(self.learning_data)
        }

class RobotManager:
    """Gestor principal de robots"""
    
    def __init__(self):
        self.robots: Dict[str, VirtualRobot] = {}
        self.active_robots_count = 0
        self.total_tasks_assigned = 0
        self.running = False
        
        logger.info("Robot Manager inicializado")
    
    async def create_robot(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Crear un nuevo robot"""
        robot_type = RobotType(config.get("type", "maintenance"))
        robot = VirtualRobot(robot_type, config)
        
        self.robots[robot.id] = robot
        self.active_robots_count += 1
        
        # Iniciar loop de actualización para el robot
        asyncio.create_task(self._robot_update_loop(robot))
        
        logger.info(f"Robot creado: {robot.name} ({robot.type.value})")
        return robot.to_dict()
    
    async def get_robot(self, robot_id: str) -> Optional[Dict[str, Any]]:
        """Obtener información de un robot específico"""
        robot = self.robots.get(robot_id)
        return robot.to_dict() if robot else None
    
    async def get_all_robots(self) -> List[Dict[str, Any]]:
        """Obtener lista de todos los robots"""
        return [robot.to_dict() for robot in self.robots.values()]
    
    async def get_robot_count(self) -> int:
        """Obtener número total de robots activos"""
        return len(self.robots)
    
    async def send_command(self, robot_id: str, command: Dict[str, Any]) -> Dict[str, Any]:
        """Enviar comando a un robot específico"""
        robot = self.robots.get(robot_id)
        
        if not robot:
            return {"success": False, "error": "Robot no encontrado"}
        
        command_type = command.get("type")
        
        try:
            if command_type == "move":
                await self._handle_move_command(robot, command)
            elif command_type == "task":
                await robot.add_task(command.get("task", {}))
            elif command_type == "stop":
                robot.current_task = None
                robot.status = RobotStatus.IDLE
            elif command_type == "charge":
                await robot.start_charging()
            else:
                return {"success": False, "error": f"Comando desconocido: {command_type}"}
            
            return {"success": True, "robot_status": robot.to_dict()}
            
        except Exception as e:
            logger.error(f"Error ejecutando comando en robot {robot_id}: {e}")
            return {"success": False, "error": str(e)}
    
    async def _handle_move_command(self, robot: VirtualRobot, command: Dict):
        """Manejar comando de movimiento"""
        target = command.get("target", {})
        
        if "x" in target:
            robot.position.x = target["x"]
        if "y" in target:
            robot.position.y = target["y"]
        if "z" in target:
            robot.position.z = target["z"]
        
        # Simular consumo de energía por movimiento
        distance = command.get("distance", 1.0)
        energy_cost = distance * (1.0 - robot.capabilities.energy_efficiency) * 2.0
        robot.energy_level = max(0.0, robot.energy_level - energy_cost)
        
        logger.info(f"Robot {robot.name} se movió a posición ({robot.position.x}, {robot.position.y}, {robot.position.z})")
    
    async def _robot_update_loop(self, robot: VirtualRobot):
        """Loop de actualización para un robot individual"""
        while robot.id in self.robots:
            try:
                await robot.update()
                await asyncio.sleep(1)  # Actualizar cada segundo
            except Exception as e:
                logger.error(f"Error actualizando robot {robot.name}: {e}")
                await asyncio.sleep(5)  # Esperar más tiempo si hay error
    
    async def delete_robot(self, robot_id: str) -> bool:
        """Eliminar un robot del sistema"""
        if robot_id in self.robots:
            robot = self.robots[robot_id]
            logger.info(f"Eliminando robot: {robot.name}")
            del self.robots[robot_id]
            self.active_robots_count -= 1
            return True
        return False
    
    async def get_system_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del sistema de robots"""
        if not self.robots:
            return {
                "total_robots": 0,
                "active_robots": 0,
                "average_efficiency": 0.0,
                "total_tasks_completed": 0,
                "average_energy": 0.0
            }
        
        total_efficiency = sum(robot.stats.efficiency_rating for robot in self.robots.values())
        total_tasks = sum(robot.stats.tasks_completed for robot in self.robots.values())
        total_energy = sum(robot.energy_level for robot in self.robots.values())
        active_count = sum(1 for robot in self.robots.values() if robot.status == RobotStatus.ACTIVE)
        
        return {
            "total_robots": len(self.robots),
            "active_robots": active_count,
            "average_efficiency": total_efficiency / len(self.robots),
            "total_tasks_completed": total_tasks,
            "average_energy": total_energy / len(self.robots),
            "robots_by_type": self._get_robots_by_type(),
            "robots_by_status": self._get_robots_by_status()
        }
    
    def _get_robots_by_type(self) -> Dict[str, int]:
        """Contar robots por tipo"""
        type_counts = {}
        for robot in self.robots.values():
            robot_type = robot.type.value
            type_counts[robot_type] = type_counts.get(robot_type, 0) + 1
        return type_counts
    
    def _get_robots_by_status(self) -> Dict[str, int]:
        """Contar robots por estado"""
        status_counts = {}
        for robot in self.robots.values():
            status = robot.status.value
            status_counts[status] = status_counts.get(status, 0) + 1
        return status_counts