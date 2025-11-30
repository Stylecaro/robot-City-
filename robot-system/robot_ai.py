"""
Robot AI System - Sistema de Inteligencia Artificial para Robots
Implementa pathfinding, comportamientos autónomos y aprendizaje
"""
import numpy as np
import asyncio
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import heapq
from datetime import datetime
import logging


class BehaviorState(Enum):
    """Estados de comportamiento del robot"""
    IDLE = "idle"
    PATROL = "patrol"
    WORK = "work"
    CHARGE = "charge"
    MAINTENANCE = "maintenance"
    EMERGENCY = "emergency"
    LEARN = "learn"


class TaskPriority(Enum):
    """Prioridades de tareas"""
    CRITICAL = 5
    HIGH = 4
    NORMAL = 3
    LOW = 2
    OPTIONAL = 1


@dataclass
class Position:
    """Posición 3D en el mundo"""
    x: float
    y: float
    z: float
    
    def distance_to(self, other: 'Position') -> float:
        """Calcula distancia euclidiana"""
        return np.sqrt((self.x - other.x)**2 + 
                      (self.y - other.y)**2 + 
                      (self.z - other.z)**2)
    
    def to_tuple(self) -> Tuple[float, float, float]:
        return (self.x, self.y, self.z)


@dataclass
class Task:
    """Tarea para un robot"""
    task_id: str
    task_type: str
    target_position: Position
    priority: TaskPriority
    deadline: Optional[datetime] = None
    requirements: Dict[str, Any] = field(default_factory=dict)
    progress: float = 0.0
    completed: bool = False


@dataclass
class Obstacle:
    """Obstáculo en el mapa"""
    position: Position
    radius: float
    height: float


class PathFinder:
    """Sistema de pathfinding A* optimizado"""
    
    def __init__(self, grid_size: int = 200, cell_size: float = 1.0):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.obstacles: List[Obstacle] = []
        self.grid = np.zeros((grid_size, grid_size), dtype=bool)
        
    def add_obstacle(self, obstacle: Obstacle):
        """Añade obstáculo al mapa"""
        self.obstacles.append(obstacle)
        self._update_grid()
    
    def _update_grid(self):
        """Actualiza grid con obstáculos"""
        self.grid.fill(False)
        
        for obstacle in self.obstacles:
            # Marcar celdas ocupadas
            cx = int((obstacle.position.x + self.grid_size * self.cell_size / 2) / self.cell_size)
            cy = int((obstacle.position.z + self.grid_size * self.cell_size / 2) / self.cell_size)
            radius_cells = int(obstacle.radius / self.cell_size) + 1
            
            for dx in range(-radius_cells, radius_cells + 1):
                for dy in range(-radius_cells, radius_cells + 1):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                        if dx*dx + dy*dy <= radius_cells*radius_cells:
                            self.grid[nx, ny] = True
    
    def find_path(self, start: Position, goal: Position) -> List[Position]:
        """Encuentra camino usando A*"""
        # Convertir a coordenadas de grid
        start_grid = self._world_to_grid(start)
        goal_grid = self._world_to_grid(goal)
        
        if not self._is_valid(start_grid) or not self._is_valid(goal_grid):
            return [start, goal]  # Camino directo si no hay grid válido
        
        # A* algorithm
        open_set = []
        heapq.heappush(open_set, (0, start_grid))
        
        came_from = {}
        g_score = {start_grid: 0}
        f_score = {start_grid: self._heuristic(start_grid, goal_grid)}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == goal_grid:
                return self._reconstruct_path(came_from, current)
            
            for neighbor in self._get_neighbors(current):
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, goal_grid)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        # No path found
        return [start, goal]
    
    def _world_to_grid(self, pos: Position) -> Tuple[int, int]:
        """Convierte posición del mundo a coordenadas de grid"""
        x = int((pos.x + self.grid_size * self.cell_size / 2) / self.cell_size)
        z = int((pos.z + self.grid_size * self.cell_size / 2) / self.cell_size)
        return (x, z)
    
    def _grid_to_world(self, grid_pos: Tuple[int, int]) -> Position:
        """Convierte coordenadas de grid a posición del mundo"""
        x = grid_pos[0] * self.cell_size - self.grid_size * self.cell_size / 2
        z = grid_pos[1] * self.cell_size - self.grid_size * self.cell_size / 2
        return Position(x, 0, z)
    
    def _is_valid(self, grid_pos: Tuple[int, int]) -> bool:
        """Verifica si una posición de grid es válida"""
        x, z = grid_pos
        if x < 0 or x >= self.grid_size or z < 0 or z >= self.grid_size:
            return False
        return not self.grid[x, z]
    
    def _get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Obtiene vecinos válidos (8 direcciones)"""
        x, z = pos
        neighbors = []
        
        for dx, dz in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (-1,1), (1,-1), (1,1)]:
            nx, nz = x + dx, z + dz
            if self._is_valid((nx, nz)):
                neighbors.append((nx, nz))
        
        return neighbors
    
    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Heurística para A* (distancia Manhattan)"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def _reconstruct_path(self, came_from: Dict, current: Tuple[int, int]) -> List[Position]:
        """Reconstruye el camino desde came_from"""
        path = [self._grid_to_world(current)]
        
        while current in came_from:
            current = came_from[current]
            path.append(self._grid_to_world(current))
        
        path.reverse()
        return path


class BehaviorTree:
    """Árbol de comportamiento para toma de decisiones"""
    
    def __init__(self, robot: 'RobotAI'):
        self.robot = robot
    
    async def evaluate(self) -> BehaviorState:
        """Evalúa el árbol y retorna el estado apropiado"""
        # Prioridad 1: Emergencias
        if await self._check_emergency():
            return BehaviorState.EMERGENCY
        
        # Prioridad 2: Batería baja
        if self.robot.battery_level < 0.2:
            return BehaviorState.CHARGE
        
        # Prioridad 3: Mantenimiento necesario
        if self.robot.health < 0.5:
            return BehaviorState.MAINTENANCE
        
        # Prioridad 4: Tareas pendientes
        if self.robot.task_queue:
            return BehaviorState.WORK
        
        # Prioridad 5: Aprendizaje si hay tiempo
        if self.robot.learning_enabled and np.random.random() < 0.1:
            return BehaviorState.LEARN
        
        # Prioridad 6: Patrullar
        if self.robot.robot_type in ['security', 'maintenance']:
            return BehaviorState.PATROL
        
        # Default: Idle
        return BehaviorState.IDLE
    
    async def _check_emergency(self) -> bool:
        """Verifica situaciones de emergencia"""
        # Batería crítica
        if self.robot.battery_level < 0.05:
            return True
        
        # Daño crítico
        if self.robot.health < 0.2:
            return True
        
        # Tareas críticas pendientes
        critical_tasks = [t for t in self.robot.task_queue 
                         if t.priority == TaskPriority.CRITICAL]
        if critical_tasks:
            return True
        
        return False


class LearningModule:
    """Módulo de aprendizaje por refuerzo para robots"""
    
    def __init__(self):
        self.q_table: Dict[Tuple, Dict[str, float]] = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.epsilon = 0.1  # Exploración
        
        self.episode_rewards: List[float] = []
        self.total_experiences = 0
    
    def get_action(self, state: Tuple, available_actions: List[str]) -> str:
        """Selecciona acción usando epsilon-greedy"""
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in available_actions}
        
        # Exploración vs Explotación
        if np.random.random() < self.epsilon:
            return np.random.choice(available_actions)
        else:
            # Mejor acción conocida
            return max(self.q_table[state], key=self.q_table[state].get)
    
    def update(self, state: Tuple, action: str, reward: float, next_state: Tuple):
        """Actualiza Q-table con experiencia"""
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0}
        
        if next_state not in self.q_table:
            self.q_table[next_state] = {action: 0.0}
        
        # Q-learning update
        old_value = self.q_table[state].get(action, 0.0)
        next_max = max(self.q_table[next_state].values()) if self.q_table[next_state] else 0.0
        
        new_value = old_value + self.learning_rate * (reward + self.discount_factor * next_max - old_value)
        self.q_table[state][action] = new_value
        
        self.total_experiences += 1
        
        # Decaimiento de epsilon (menos exploración con el tiempo)
        self.epsilon = max(0.01, self.epsilon * 0.9995)
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de aprendizaje"""
        return {
            'total_experiences': self.total_experiences,
            'states_learned': len(self.q_table),
            'epsilon': self.epsilon,
            'avg_reward': np.mean(self.episode_rewards[-100:]) if self.episode_rewards else 0.0
        }


class RobotAI:
    """Robot autónomo con IA"""
    
    def __init__(self, robot_id: str, robot_type: str, start_position: Position):
        self.robot_id = robot_id
        self.robot_type = robot_type
        self.position = start_position
        
        # Estado
        self.state = BehaviorState.IDLE
        self.battery_level = 1.0
        self.health = 1.0
        self.speed = 5.0  # unidades/segundo
        
        # Sistemas
        self.pathfinder = PathFinder()
        self.behavior_tree = BehaviorTree(self)
        self.learning_module = LearningModule()
        
        # Tareas
        self.task_queue: List[Task] = []
        self.current_task: Optional[Task] = None
        self.current_path: List[Position] = []
        
        # Configuración
        self.learning_enabled = True
        self.auto_recharge = True
        self.max_speed = 10.0
        
        # Estadísticas
        self.tasks_completed = 0
        self.distance_traveled = 0.0
        self.time_active = 0.0
        
        self.logger = logging.getLogger(f"RobotAI.{robot_id}")
        self.active = False
    
    async def start(self):
        """Inicia el robot"""
        self.active = True
        self.logger.info(f"🤖 Robot {self.robot_id} iniciado en {self.position.to_tuple()}")
        
        # Loop principal
        await asyncio.gather(
            self._behavior_loop(),
            self._movement_loop(),
            self._maintenance_loop()
        )
    
    async def stop(self):
        """Detiene el robot"""
        self.active = False
        self.logger.info(f"🛑 Robot {self.robot_id} detenido")
    
    async def _behavior_loop(self):
        """Loop de comportamiento (evalúa cada segundo)"""
        while self.active:
            try:
                # Evaluar árbol de comportamiento
                new_state = await self.behavior_tree.evaluate()
                
                if new_state != self.state:
                    self.logger.info(f"🔄 {self.robot_id}: {self.state.value} → {new_state.value}")
                    self.state = new_state
                
                # Ejecutar comportamiento actual
                await self._execute_behavior()
                
                await asyncio.sleep(1.0)
            except Exception as e:
                self.logger.error(f"Error en behavior loop: {e}")
                await asyncio.sleep(1.0)
    
    async def _execute_behavior(self):
        """Ejecuta el comportamiento actual"""
        if self.state == BehaviorState.IDLE:
            await self._idle_behavior()
        elif self.state == BehaviorState.PATROL:
            await self._patrol_behavior()
        elif self.state == BehaviorState.WORK:
            await self._work_behavior()
        elif self.state == BehaviorState.CHARGE:
            await self._charge_behavior()
        elif self.state == BehaviorState.MAINTENANCE:
            await self._maintenance_behavior()
        elif self.state == BehaviorState.EMERGENCY:
            await self._emergency_behavior()
        elif self.state == BehaviorState.LEARN:
            await self._learn_behavior()
    
    async def _idle_behavior(self):
        """Comportamiento en idle"""
        # Esperar nuevas tareas
        pass
    
    async def _patrol_behavior(self):
        """Comportamiento de patrulla"""
        if not self.current_path:
            # Generar punto aleatorio de patrulla
            target = Position(
                np.random.uniform(-90, 90),
                0,
                np.random.uniform(-90, 90)
            )
            self.current_path = self.pathfinder.find_path(self.position, target)
    
    async def _work_behavior(self):
        """Comportamiento de trabajo"""
        if not self.current_task and self.task_queue:
            # Tomar siguiente tarea (ordenar por prioridad)
            self.task_queue.sort(key=lambda t: t.priority.value, reverse=True)
            self.current_task = self.task_queue.pop(0)
            
            # Calcular camino a la tarea
            self.current_path = self.pathfinder.find_path(
                self.position, 
                self.current_task.target_position
            )
            
            self.logger.info(f"📋 {self.robot_id}: Iniciando tarea {self.current_task.task_id}")
        
        elif self.current_task:
            # Trabajar en tarea actual
            if self.position.distance_to(self.current_task.target_position) < 2.0:
                # En posición, ejecutar tarea
                self.current_task.progress += 0.1
                
                if self.current_task.progress >= 1.0:
                    self.current_task.completed = True
                    self.tasks_completed += 1
                    
                    # Recompensa de aprendizaje
                    reward = self._calculate_task_reward(self.current_task)
                    self.learning_module.episode_rewards.append(reward)
                    
                    self.logger.info(f"✅ {self.robot_id}: Tarea completada - {self.current_task.task_id}")
                    self.current_task = None
    
    async def _charge_behavior(self):
        """Comportamiento de carga"""
        # Buscar estación de carga más cercana
        if not self.current_path:
            charge_station = Position(0, 0, 0)  # Estación central
            self.current_path = self.pathfinder.find_path(self.position, charge_station)
        
        # Si está en estación, cargar
        if self.position.distance_to(Position(0, 0, 0)) < 5.0:
            self.battery_level = min(1.0, self.battery_level + 0.05)
            if self.battery_level > 0.9:
                self.logger.info(f"🔋 {self.robot_id}: Batería cargada")
                self.current_path = []
    
    async def _maintenance_behavior(self):
        """Comportamiento de mantenimiento"""
        # Auto-reparación
        self.health = min(1.0, self.health + 0.02)
        if self.health > 0.9:
            self.logger.info(f"🔧 {self.robot_id}: Mantenimiento completado")
    
    async def _emergency_behavior(self):
        """Comportamiento de emergencia"""
        self.logger.warning(f"🚨 {self.robot_id}: MODO EMERGENCIA")
        
        # Forzar carga/reparación
        if self.battery_level < 0.1:
            await self._charge_behavior()
        if self.health < 0.3:
            await self._maintenance_behavior()
    
    async def _learn_behavior(self):
        """Comportamiento de aprendizaje"""
        # Practicar tareas simuladas para mejorar
        simulated_state = (self.state.value, self.battery_level > 0.5, len(self.task_queue))
        action = self.learning_module.get_action(simulated_state, ['move', 'work', 'wait'])
        
        # Simular resultado
        reward = np.random.uniform(-0.1, 0.3)
        next_state = (BehaviorState.IDLE.value, self.battery_level > 0.5, len(self.task_queue))
        
        self.learning_module.update(simulated_state, action, reward, next_state)
    
    async def _movement_loop(self):
        """Loop de movimiento (actualiza 10 veces por segundo)"""
        while self.active:
            try:
                if self.current_path and len(self.current_path) > 0:
                    target = self.current_path[0]
                    distance = self.position.distance_to(target)
                    
                    if distance < 0.5:
                        # Alcanzó waypoint
                        self.current_path.pop(0)
                    else:
                        # Mover hacia waypoint
                        direction_x = (target.x - self.position.x) / distance
                        direction_z = (target.z - self.position.z) / distance
                        
                        move_distance = min(self.speed * 0.1, distance)
                        self.position.x += direction_x * move_distance
                        self.position.z += direction_z * move_distance
                        
                        self.distance_traveled += move_distance
                
                await asyncio.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Error en movement loop: {e}")
                await asyncio.sleep(0.1)
    
    async def _maintenance_loop(self):
        """Loop de mantenimiento (actualiza cada 5 segundos)"""
        while self.active:
            try:
                # Degradación natural
                if self.state != BehaviorState.IDLE:
                    self.battery_level = max(0, self.battery_level - 0.005)
                    self.health = max(0, self.health - 0.001)
                
                self.time_active += 5.0
                
                await asyncio.sleep(5.0)
            except Exception as e:
                self.logger.error(f"Error en maintenance loop: {e}")
                await asyncio.sleep(5.0)
    
    def _calculate_task_reward(self, task: Task) -> float:
        """Calcula recompensa por completar tarea"""
        reward = 1.0
        
        # Bonificación por prioridad
        reward += task.priority.value * 0.2
        
        # Bonificación por eficiencia de batería
        reward += self.battery_level * 0.5
        
        # Penalización por daño
        reward -= (1.0 - self.health) * 0.3
        
        return reward
    
    def add_task(self, task: Task):
        """Añade tarea a la cola"""
        self.task_queue.append(task)
        self.logger.info(f"📥 {self.robot_id}: Nueva tarea - {task.task_id} (prioridad: {task.priority.name})")
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene estado completo del robot"""
        return {
            'robot_id': self.robot_id,
            'robot_type': self.robot_type,
            'position': self.position.to_tuple(),
            'state': self.state.value,
            'battery_level': self.battery_level,
            'health': self.health,
            'tasks_in_queue': len(self.task_queue),
            'current_task': self.current_task.task_id if self.current_task else None,
            'tasks_completed': self.tasks_completed,
            'distance_traveled': self.distance_traveled,
            'time_active': self.time_active,
            'learning_stats': self.learning_module.get_stats()
        }


# Funciones de utilidad
async def create_robot(robot_type: str, position: Optional[Position] = None) -> RobotAI:
    """Crea un nuevo robot"""
    if position is None:
        position = Position(
            np.random.uniform(-50, 50),
            0,
            np.random.uniform(-50, 50)
        )
    
    robot_id = f"{robot_type}_{np.random.randint(1000, 9999)}"
    robot = RobotAI(robot_id, robot_type, position)
    
    return robot


async def main():
    """Función de prueba"""
    logging.basicConfig(level=logging.INFO)
    
    print("🤖 Iniciando sistema de robots inteligentes...")
    
    # Crear robots de prueba
    robots = []
    for robot_type in ['manufacturing', 'security', 'research']:
        robot = await create_robot(robot_type)
        robots.append(robot)
        
        # Añadir tareas de prueba
        task = Task(
            task_id=f"task_{len(robots)}",
            task_type="test",
            target_position=Position(
                np.random.uniform(-80, 80),
                0,
                np.random.uniform(-80, 80)
            ),
            priority=TaskPriority.NORMAL
        )
        robot.add_task(task)
    
    # Iniciar robots
    try:
        await asyncio.gather(*[robot.start() for robot in robots])
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo robots...")
        for robot in robots:
            await robot.stop()


if __name__ == "__main__":
    asyncio.run(main())
