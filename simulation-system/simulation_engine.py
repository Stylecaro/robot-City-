"""
Simulation System - Simulaciones de entrenamiento y pruebas para robots
Training grounds, scenarios, performance testing
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import uuid
import random


class SimulationType(Enum):
    """Tipos de simulación"""
    COMBAT = "combat"          # Combate contra IA
    OBSTACLE = "obstacle"      # Evasión de obstáculos
    SURVIVAL = "survival"      # Supervivencia
    SPEED_RUN = "speed_run"    # Carrera contra reloj
    DEFENSE = "defense"        # Defensa contra olas
    PRECISION = "precision"    # Precisión de armas
    STEALTH = "stealth"        # Sigilo
    ENDURANCE = "endurance"    # Resistencia


class DifficultyLevel(Enum):
    """Niveles de dificultad"""
    EASY = 1
    NORMAL = 2
    HARD = 3
    EXPERT = 4
    NIGHTMARE = 5


@dataclass
class SimulationScenario:
    """Escenario de simulación"""
    scenario_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    sim_type: SimulationType = SimulationType.COMBAT
    difficulty: DifficultyLevel = DifficultyLevel.NORMAL
    
    # Parámetros
    duration_seconds: int = 300  # 5 minutos
    enemy_count: int = 1
    objectives: List[str] = field(default_factory=list)
    
    # Rewards
    exp_reward: int = 100
    credits_reward: int = 500
    
    # Descripción
    environment: str = ""  # Desierto, laboratorio, ciudad, etc.
    
    def to_dict(self) -> Dict:
        return {
            "scenario_id": self.scenario_id,
            "name": self.name,
            "type": self.sim_type.value,
            "difficulty": self.difficulty.name,
            "duration": self.duration_seconds,
            "enemies": self.enemy_count,
            "exp_reward": self.exp_reward,
            "credits_reward": self.credits_reward
        }


@dataclass
class SimulationResult:
    """Resultado de una simulación"""
    result_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    scenario_id: str = ""
    robot_id: str = ""
    
    # Resultados
    completed: bool = False
    time_taken: float = 0.0
    accuracy: float = 0.0  # 0-100%
    damage_taken: int = 0
    enemies_defeated: int = 0
    objectives_completed: int = 0
    
    # Rewards
    exp_gained: int = 0
    credits_gained: int = 0
    
    # Timestamp
    completed_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "scenario": self.scenario_id,
            "robot": self.robot_id,
            "completed": self.completed,
            "time_taken": round(self.time_taken, 2),
            "accuracy": round(self.accuracy, 2),
            "damage_taken": self.damage_taken,
            "enemies_defeated": self.enemies_defeated,
            "exp_gained": self.exp_gained,
            "credits_gained": self.credits_gained
        }


class SimulationEngine:
    """Motor de simulaciones"""
    
    def __init__(self):
        self.scenarios: Dict[str, SimulationScenario] = {}
        self.results: List[SimulationResult] = []
        self.active_simulations: Dict[str, SimulationResult] = {}  # robot_id -> resultado
        
        # Crear escenarios base
        self._init_scenarios()
    
    def _init_scenarios(self):
        """Inicializa escenarios de simulación"""
        scenarios = [
            # COMBAT
            SimulationScenario(
                name="Single Combat",
                description="Batalla 1v1 contra enemigo",
                sim_type=SimulationType.COMBAT,
                difficulty=DifficultyLevel.NORMAL,
                duration_seconds=300,
                enemy_count=1,
                objectives=["Defeat enemy"],
                exp_reward=100,
                credits_reward=500,
                environment="Arena"
            ),
            SimulationScenario(
                name="Wave Combat",
                description="Batalla contra olas de enemigos",
                sim_type=SimulationType.COMBAT,
                difficulty=DifficultyLevel.HARD,
                duration_seconds=600,
                enemy_count=5,
                objectives=["Survive 5 waves"],
                exp_reward=250,
                credits_reward=1500,
                environment="Fortress"
            ),
            # OBSTACLE
            SimulationScenario(
                name="Obstacle Course",
                description="Carrera por circuito de obstáculos",
                sim_type=SimulationType.OBSTACLE,
                difficulty=DifficultyLevel.NORMAL,
                duration_seconds=180,
                objectives=["Complete course"],
                exp_reward=75,
                credits_reward=400,
                environment="Training Ground"
            ),
            # SURVIVAL
            SimulationScenario(
                name="Desert Survival",
                description="Supervivencia en desierto",
                sim_type=SimulationType.SURVIVAL,
                difficulty=DifficultyLevel.HARD,
                duration_seconds=900,
                enemy_count=3,
                objectives=["Survive 15 minutes", "Collect supplies"],
                exp_reward=200,
                credits_reward=1000,
                environment="Desert"
            ),
            # SPEED RUN
            SimulationScenario(
                name="Speed Challenge",
                description="Completar objetivos rápidamente",
                sim_type=SimulationType.SPEED_RUN,
                difficulty=DifficultyLevel.NORMAL,
                duration_seconds=120,
                objectives=["Complete under 2 minutes"],
                exp_reward=150,
                credits_reward=800,
                environment="City"
            ),
            # DEFENSE
            SimulationScenario(
                name="Tower Defense",
                description="Defender posición contra oleadas",
                sim_type=SimulationType.DEFENSE,
                difficulty=DifficultyLevel.HARD,
                duration_seconds=600,
                enemy_count=10,
                objectives=["Survive all waves"],
                exp_reward=300,
                credits_reward=2000,
                environment="Fortress"
            ),
            # STEALTH
            SimulationScenario(
                name="Stealth Mission",
                description="Infiltración sin ser detectado",
                sim_type=SimulationType.STEALTH,
                difficulty=DifficultyLevel.EXPERT,
                duration_seconds=300,
                objectives=["Complete objective undetected"],
                exp_reward=200,
                credits_reward=1200,
                environment="Research Lab"
            ),
            # ENDURANCE
            SimulationScenario(
                name="Endurance Test",
                description="Prueba de resistencia prolongada",
                sim_type=SimulationType.ENDURANCE,
                difficulty=DifficultyLevel.HARD,
                duration_seconds=1200,
                objectives=["Survive 20 minutes"],
                exp_reward=400,
                credits_reward=2500,
                environment="Arena"
            ),
        ]
        
        for scenario in scenarios:
            self.scenarios[scenario.scenario_id] = scenario
    
    def get_scenario(self, scenario_id: str) -> Optional[SimulationScenario]:
        """Obtiene escenario"""
        return self.scenarios.get(scenario_id)
    
    def get_all_scenarios(self) -> List[SimulationScenario]:
        """Lista todos los escenarios"""
        return list(self.scenarios.values())
    
    def get_scenarios_by_type(self, sim_type: SimulationType) -> List[SimulationScenario]:
        """Obtiene escenarios por tipo"""
        return [s for s in self.scenarios.values() if s.sim_type == sim_type]
    
    def get_scenarios_by_difficulty(self, difficulty: DifficultyLevel) -> List[SimulationScenario]:
        """Obtiene escenarios por dificultad"""
        return [s for s in self.scenarios.values() if s.difficulty == difficulty]
    
    def start_simulation(self, robot_id: str, scenario_id: str) -> Optional[SimulationResult]:
        """Inicia una simulación"""
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            return None
        
        result = SimulationResult(
            scenario_id=scenario_id,
            robot_id=robot_id
        )
        
        self.active_simulations[robot_id] = result
        return result
    
    def simulate_performance(self, robot_id: str, scenario_id: str, 
                           robot_stats: Dict) -> SimulationResult:
        """Simula la ejecución de un escenario"""
        scenario = self.get_scenario(scenario_id)
        if not scenario:
            return None
        
        # Iniciar resultado
        result = SimulationResult(
            scenario_id=scenario_id,
            robot_id=robot_id
        )
        
        # Simulación básica basada en stats
        attack = robot_stats.get("attack", 50)
        defense = robot_stats.get("defense", 50)
        speed = robot_stats.get("speed", 50)
        intelligence = robot_stats.get("intelligence", 50)
        
        # Cálculo de desempeño
        base_success_rate = 0.5 + (attack * 0.003) + (intelligence * 0.002)
        base_success_rate = min(0.95, base_success_rate)  # Cap at 95%
        
        # Éxito de la simulación
        success = random.random() < base_success_rate
        result.completed = success
        
        # Tiempo (más velocidad = más rápido)
        time_factor = 1.0 - (speed / 500)  # 50 = factor 0.9, 100 = factor 0.8
        result.time_taken = scenario.duration_seconds * time_factor
        
        # Precisión (basada en ataque)
        result.accuracy = min(100.0, (attack / 100) * 100)
        
        # Daño recibido (menos con defensa alta)
        base_damage = scenario.difficulty.value * 30
        damage_reduction = 1.0 - (defense / 500)
        result.damage_taken = max(1, int(base_damage * damage_reduction))
        
        # Enemigos derrotados
        if success:
            result.enemies_defeated = scenario.enemy_count
            result.objectives_completed = len(scenario.objectives)
        else:
            result.enemies_defeated = max(0, scenario.enemy_count // 2)
            result.objectives_completed = max(0, len(scenario.objectives) // 2)
        
        # Rewards
        success_multiplier = 1.5 if success else 0.5
        result.exp_gained = int(scenario.exp_reward * success_multiplier)
        result.credits_gained = int(scenario.credits_reward * success_multiplier)
        
        # Guardar resultado
        self.results.append(result)
        if robot_id in self.active_simulations:
            del self.active_simulations[robot_id]
        
        return result
    
    def get_robot_stats(self, robot_id: str) -> Dict:
        """Obtiene estadísticas de entrenamiento de un robot"""
        robot_results = [r for r in self.results if r.robot_id == robot_id]
        
        if not robot_results:
            return {
                "robot_id": robot_id,
                "simulations_completed": 0,
                "success_rate": 0.0,
                "average_accuracy": 0.0
            }
        
        completed = sum(1 for r in robot_results if r.completed)
        avg_accuracy = sum(r.accuracy for r in robot_results) / len(robot_results)
        
        return {
            "robot_id": robot_id,
            "simulations_completed": len(robot_results),
            "success_rate": round((completed / len(robot_results)) * 100, 2),
            "average_accuracy": round(avg_accuracy, 2),
            "total_exp_gained": sum(r.exp_gained for r in robot_results),
            "total_credits_gained": sum(r.credits_gained for r in robot_results)
        }
    
    def get_leaderboard(self, limit: int = 50) -> List[Dict]:
        """Obtiene leaderboard de entrenamiento"""
        # Agrupar por robot
        robot_scores = {}
        for result in self.results:
            if result.robot_id not in robot_scores:
                robot_scores[result.robot_id] = {
                    "completed": 0,
                    "total_exp": 0,
                    "avg_accuracy": 0.0
                }
            
            if result.completed:
                robot_scores[result.robot_id]["completed"] += 1
            robot_scores[result.robot_id]["total_exp"] += result.exp_gained
        
        # Calcular promedio de precisión
        for robot_id in robot_scores:
            robot_results = [r for r in self.results if r.robot_id == robot_id]
            robot_scores[robot_id]["avg_accuracy"] = (
                sum(r.accuracy for r in robot_results) / len(robot_results)
                if robot_results else 0.0
            )
        
        # Ordenar por XP total
        sorted_scores = sorted(
            robot_scores.items(),
            key=lambda x: x[1]["total_exp"],
            reverse=True
        )[:limit]
        
        return [
            {
                "rank": i + 1,
                "robot_id": rid,
                "simulations_completed": scores["completed"],
                "total_exp": scores["total_exp"],
                "average_accuracy": round(scores["avg_accuracy"], 2)
            }
            for i, (rid, scores) in enumerate(sorted_scores)
        ]
    
    def get_global_stats(self) -> Dict:
        """Obtiene estadísticas globales"""
        if not self.results:
            return {
                "total_simulations": 0,
                "success_rate": 0.0,
                "total_exp_gained": 0,
                "by_type": {}
            }
        
        completed = sum(1 for r in self.results if r.completed)
        
        # Por tipo
        by_type = {}
        for scenario_id, scenario in self.scenarios.items():
            scenario_results = [r for r in self.results if r.scenario_id == scenario_id]
            if scenario_results:
                by_type[scenario.sim_type.value] = {
                    "runs": len(scenario_results),
                    "success_rate": sum(1 for r in scenario_results if r.completed) / len(scenario_results) * 100
                }
        
        return {
            "total_simulations": len(self.results),
            "success_rate": round((completed / len(self.results)) * 100, 2),
            "total_exp_gained": sum(r.exp_gained for r in self.results),
            "unique_robots": len(set(r.robot_id for r in self.results)),
            "by_type": by_type
        }


# Instancia global
simulation_engine = SimulationEngine()
