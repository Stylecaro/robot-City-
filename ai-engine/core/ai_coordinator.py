"""
AI Coordinator - Sistema Central de Inteligencia Artificial
Optimiza y coordina todos los sistemas del Metaverso Ciudad Robot
"""
import numpy as np
import asyncio
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging

try:
    import tensorflow as tf
    from tensorflow import keras
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logging.warning("TensorFlow no disponible - modo básico activado")

try:
    import torch
    import torch.nn as nn
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    logging.warning("PyTorch no disponible - modo básico activado")


@dataclass
class CityMetrics:
    """Métricas de la ciudad en tiempo real"""
    timestamp: str
    total_robots: int
    active_robots: int
    manufacturing_efficiency: float
    research_progress: float
    security_level: float
    energy_consumption: float
    traffic_density: float
    citizen_satisfaction: float
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class RobotState:
    """Estado de un robot individual"""
    robot_id: str
    type: str  # 'manufacturing', 'research', 'security', 'maintenance'
    position: tuple
    status: str  # 'idle', 'working', 'charging', 'maintenance'
    battery_level: float
    task_queue: List[str]
    performance_score: float
    
    def to_dict(self) -> Dict:
        return asdict(self)


class NeuralOptimizer:
    """Red neuronal para optimización de recursos"""
    
    def __init__(self):
        self.model = None
        self.is_trained = False
        
        if TENSORFLOW_AVAILABLE:
            self._build_tensorflow_model()
        elif TORCH_AVAILABLE:
            self._build_torch_model()
        else:
            logging.warning("No hay framework de ML disponible - usando optimización clásica")
    
    def _build_tensorflow_model(self):
        """Construye modelo con TensorFlow"""
        self.model = keras.Sequential([
            keras.layers.Dense(128, activation='relu', input_shape=(10,)),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(64, activation='relu'),
            keras.layers.Dropout(0.2),
            keras.layers.Dense(32, activation='relu'),
            keras.layers.Dense(5, activation='softmax')  # 5 decisiones de optimización
        ])
        self.model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        logging.info("✅ Modelo TensorFlow creado")
    
    def _build_torch_model(self):
        """Construye modelo con PyTorch"""
        class OptimizationNet(nn.Module):
            def __init__(self):
                super().__init__()
                self.layers = nn.Sequential(
                    nn.Linear(10, 128),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(128, 64),
                    nn.ReLU(),
                    nn.Dropout(0.2),
                    nn.Linear(64, 32),
                    nn.ReLU(),
                    nn.Linear(32, 5),
                    nn.Softmax(dim=1)
                )
            
            def forward(self, x):
                return self.layers(x)
        
        self.model = OptimizationNet()
        logging.info("✅ Modelo PyTorch creado")
    
    def predict_optimization(self, metrics: CityMetrics) -> Dict[str, float]:
        """Predice acciones de optimización basadas en métricas"""
        # Vectorizar métricas
        features = np.array([
            metrics.total_robots / 100.0,
            metrics.active_robots / 100.0,
            metrics.manufacturing_efficiency,
            metrics.research_progress,
            metrics.security_level,
            metrics.energy_consumption,
            metrics.traffic_density,
            metrics.citizen_satisfaction,
            datetime.now().hour / 24.0,  # Hora del día
            datetime.now().weekday() / 7.0  # Día de la semana
        ]).reshape(1, -1)
        
        if self.model and TENSORFLOW_AVAILABLE:
            predictions = self.model.predict(features, verbose=0)[0]
        elif self.model and TORCH_AVAILABLE:
            with torch.no_grad():
                predictions = self.model(torch.FloatTensor(features)).numpy()[0]
        else:
            # Optimización clásica basada en reglas
            predictions = self._classical_optimization(metrics)
        
        return {
            'increase_manufacturing': float(predictions[0]),
            'boost_research': float(predictions[1]),
            'enhance_security': float(predictions[2]),
            'optimize_energy': float(predictions[3]),
            'improve_traffic': float(predictions[4])
        }
    
    def _classical_optimization(self, metrics: CityMetrics) -> np.ndarray:
        """Optimización basada en reglas cuando no hay ML"""
        scores = np.zeros(5)
        
        # Reglas heurísticas
        if metrics.manufacturing_efficiency < 0.7:
            scores[0] = 0.8  # Aumentar manufactura
        if metrics.research_progress < 0.5:
            scores[1] = 0.7  # Impulsar investigación
        if metrics.security_level < 0.6:
            scores[2] = 0.9  # Mejorar seguridad
        if metrics.energy_consumption > 0.8:
            scores[3] = 0.85  # Optimizar energía
        if metrics.traffic_density > 0.75:
            scores[4] = 0.75  # Mejorar tráfico
        
        # Normalizar
        total = scores.sum()
        if total > 0:
            scores = scores / total
        else:
            scores = np.ones(5) / 5.0
        
        return scores
    
    async def train_online(self, metrics_history: List[CityMetrics], outcomes: List[float]):
        """Entrenamiento continuo con datos nuevos"""
        if not self.model or len(metrics_history) < 10:
            return
        
        # Preparar datos de entrenamiento
        X = []
        y = []
        
        for i, metrics in enumerate(metrics_history):
            features = [
                metrics.total_robots / 100.0,
                metrics.active_robots / 100.0,
                metrics.manufacturing_efficiency,
                metrics.research_progress,
                metrics.security_level,
                metrics.energy_consumption,
                metrics.traffic_density,
                metrics.citizen_satisfaction,
                datetime.fromisoformat(metrics.timestamp).hour / 24.0,
                datetime.fromisoformat(metrics.timestamp).weekday() / 7.0
            ]
            X.append(features)
            
            # Convertir outcome a one-hot
            outcome_vector = np.zeros(5)
            outcome_vector[int(outcomes[i] * 4)] = 1.0
            y.append(outcome_vector)
        
        X = np.array(X)
        y = np.array(y)
        
        if TENSORFLOW_AVAILABLE and self.model:
            # Entrenamiento incremental
            self.model.fit(X, y, epochs=5, batch_size=32, verbose=0)
            self.is_trained = True
            logging.info("🧠 Modelo entrenado con nuevos datos")


class AICoordinator:
    """Coordinador Central de IA para Ciudad Robot"""
    
    def __init__(self):
        self.robots: Dict[str, RobotState] = {}
        self.metrics: Optional[CityMetrics] = None
        self.optimizer = NeuralOptimizer()
        self.metrics_history: List[CityMetrics] = []
        self.active = False
        
        # Configuración
        self.max_robots = 200
        self.optimal_efficiency = 0.85
        self.security_threshold = 0.7
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    async def start(self):
        """Inicia el coordinador de IA"""
        self.active = True
        self.logger.info("🤖 AI Coordinator iniciado")
        
        # Iniciar tareas en paralelo
        await asyncio.gather(
            self._monitor_city(),
            self._optimize_resources(),
            self._manage_robots(),
            self._collect_analytics()
        )
    
    async def stop(self):
        """Detiene el coordinador"""
        self.active = False
        self.logger.info("🛑 AI Coordinator detenido")
    
    async def _monitor_city(self):
        """Monitoreo continuo de la ciudad"""
        while self.active:
            try:
                # Actualizar métricas
                self.metrics = await self._calculate_metrics()
                self.metrics_history.append(self.metrics)
                
                # Mantener historial limitado (últimas 1000 entradas)
                if len(self.metrics_history) > 1000:
                    self.metrics_history = self.metrics_history[-1000:]
                
                # Log cada 30 segundos
                self.logger.info(f"📊 Métricas: Robots={self.metrics.active_robots}/{self.metrics.total_robots}, "
                               f"Eficiencia={self.metrics.manufacturing_efficiency:.2%}")
                
                await asyncio.sleep(30)
            except Exception as e:
                self.logger.error(f"Error en monitoreo: {e}")
                await asyncio.sleep(5)
    
    async def _calculate_metrics(self) -> CityMetrics:
        """Calcula métricas actuales de la ciudad"""
        active_robots = sum(1 for r in self.robots.values() if r.status in ['working', 'idle'])
        
        # Calcular promedios
        if self.robots:
            avg_performance = np.mean([r.performance_score for r in self.robots.values()])
            avg_battery = np.mean([r.battery_level for r in self.robots.values()])
        else:
            avg_performance = 0.0
            avg_battery = 1.0
        
        # Métricas simuladas (en producción vendrían de sensores reales)
        return CityMetrics(
            timestamp=datetime.now().isoformat(),
            total_robots=len(self.robots),
            active_robots=active_robots,
            manufacturing_efficiency=min(avg_performance * 1.1, 1.0),
            research_progress=np.random.uniform(0.6, 0.9),
            security_level=np.random.uniform(0.7, 0.95),
            energy_consumption=1.0 - avg_battery,
            traffic_density=active_robots / max(self.max_robots, 1),
            citizen_satisfaction=avg_performance
        )
    
    async def _optimize_resources(self):
        """Optimización inteligente de recursos"""
        while self.active:
            try:
                if not self.metrics:
                    await asyncio.sleep(10)
                    continue
                
                # Obtener recomendaciones de IA
                optimizations = self.optimizer.predict_optimization(self.metrics)
                
                # Aplicar optimizaciones
                await self._apply_optimizations(optimizations)
                
                # Log decisiones
                top_action = max(optimizations, key=optimizations.get)
                self.logger.info(f"🧠 IA sugiere: {top_action} (confianza: {optimizations[top_action]:.2%})")
                
                await asyncio.sleep(60)  # Optimizar cada minuto
            except Exception as e:
                self.logger.error(f"Error en optimización: {e}")
                await asyncio.sleep(10)
    
    async def _apply_optimizations(self, optimizations: Dict[str, float]):
        """Aplica las optimizaciones sugeridas por la IA"""
        threshold = 0.6  # Solo aplicar si confianza > 60%
        
        for action, confidence in optimizations.items():
            if confidence < threshold:
                continue
            
            if action == 'increase_manufacturing':
                await self._boost_manufacturing(confidence)
            elif action == 'boost_research':
                await self._boost_research(confidence)
            elif action == 'enhance_security':
                await self._enhance_security(confidence)
            elif action == 'optimize_energy':
                await self._optimize_energy(confidence)
            elif action == 'improve_traffic':
                await self._improve_traffic(confidence)
    
    async def _boost_manufacturing(self, intensity: float):
        """Aumenta capacidad de manufactura"""
        # Reasignar robots a manufactura
        manufacturing_robots = [r for r in self.robots.values() if r.type == 'manufacturing']
        if manufacturing_robots:
            for robot in manufacturing_robots[:int(len(manufacturing_robots) * intensity)]:
                robot.performance_score = min(robot.performance_score * 1.1, 1.0)
        self.logger.info(f"🏭 Manufactura aumentada ({intensity:.0%})")
    
    async def _boost_research(self, intensity: float):
        """Impulsa investigación"""
        research_robots = [r for r in self.robots.values() if r.type == 'research']
        if research_robots:
            for robot in research_robots[:int(len(research_robots) * intensity)]:
                robot.performance_score = min(robot.performance_score * 1.15, 1.0)
        self.logger.info(f"🔬 Investigación impulsada ({intensity:.0%})")
    
    async def _enhance_security(self, intensity: float):
        """Mejora seguridad"""
        security_robots = [r for r in self.robots.values() if r.type == 'security']
        if len(security_robots) < self.max_robots * 0.2 * intensity:
            # Crear más robots de seguridad
            await self.add_robot('security')
        self.logger.info(f"🛡️ Seguridad mejorada ({intensity:.0%})")
    
    async def _optimize_energy(self, intensity: float):
        """Optimiza consumo energético"""
        low_battery_robots = [r for r in self.robots.values() if r.battery_level < 0.3]
        for robot in low_battery_robots:
            robot.status = 'charging'
        self.logger.info(f"⚡ Energía optimizada - {len(low_battery_robots)} robots recargando")
    
    async def _improve_traffic(self, intensity: float):
        """Mejora flujo de tráfico"""
        # Redistribuir robots para evitar congestión
        for robot in list(self.robots.values())[:int(len(self.robots) * intensity)]:
            # Simular redistribución
            robot.position = (
                np.random.uniform(-100, 100),
                np.random.uniform(-100, 100),
                0
            )
        self.logger.info(f"🚦 Tráfico optimizado ({intensity:.0%})")
    
    async def _manage_robots(self):
        """Gestión automática de robots"""
        while self.active:
            try:
                # Mantener población óptima
                if len(self.robots) < self.max_robots * 0.5:
                    await self._spawn_robots(10)
                
                # Mantener robots cargados
                for robot in self.robots.values():
                    if robot.status != 'charging':
                        robot.battery_level = max(0, robot.battery_level - 0.01)
                    else:
                        robot.battery_level = min(1.0, robot.battery_level + 0.05)
                        if robot.battery_level > 0.9:
                            robot.status = 'idle'
                    
                    # Si batería crítica, forzar carga
                    if robot.battery_level < 0.2:
                        robot.status = 'charging'
                
                await asyncio.sleep(5)
            except Exception as e:
                self.logger.error(f"Error en gestión de robots: {e}")
                await asyncio.sleep(5)
    
    async def _spawn_robots(self, count: int):
        """Crea nuevos robots"""
        types = ['manufacturing', 'research', 'security', 'maintenance']
        for i in range(count):
            robot_type = np.random.choice(types)
            await self.add_robot(robot_type)
    
    async def add_robot(self, robot_type: str) -> str:
        """Añade un nuevo robot al sistema"""
        robot_id = f"robot_{len(self.robots)}_{robot_type[:3]}"
        
        robot = RobotState(
            robot_id=robot_id,
            type=robot_type,
            position=(np.random.uniform(-100, 100), np.random.uniform(-100, 100), 0),
            status='idle',
            battery_level=1.0,
            task_queue=[],
            performance_score=np.random.uniform(0.7, 0.95)
        )
        
        self.robots[robot_id] = robot
        self.logger.info(f"🤖 Nuevo robot creado: {robot_id} ({robot_type})")
        return robot_id
    
    async def remove_robot(self, robot_id: str):
        """Elimina un robot del sistema"""
        if robot_id in self.robots:
            del self.robots[robot_id]
            self.logger.info(f"🗑️ Robot eliminado: {robot_id}")
    
    async def assign_task(self, robot_id: str, task: str):
        """Asigna tarea a un robot específico"""
        if robot_id in self.robots:
            robot = self.robots[robot_id]
            robot.task_queue.append(task)
            robot.status = 'working'
            self.logger.info(f"📋 Tarea asignada a {robot_id}: {task}")
    
    async def _collect_analytics(self):
        """Recopila analíticas para entrenamiento"""
        while self.active:
            try:
                if len(self.metrics_history) > 50:
                    # Entrenar modelo con datos históricos
                    outcomes = [m.manufacturing_efficiency for m in self.metrics_history[-50:]]
                    await self.optimizer.train_online(self.metrics_history[-50:], outcomes)
                
                await asyncio.sleep(300)  # Cada 5 minutos
            except Exception as e:
                self.logger.error(f"Error en analytics: {e}")
                await asyncio.sleep(60)
    
    def get_status(self) -> Dict[str, Any]:
        """Obtiene estado completo del sistema"""
        return {
            'active': self.active,
            'total_robots': len(self.robots),
            'robots_by_type': {
                'manufacturing': len([r for r in self.robots.values() if r.type == 'manufacturing']),
                'research': len([r for r in self.robots.values() if r.type == 'research']),
                'security': len([r for r in self.robots.values() if r.type == 'security']),
                'maintenance': len([r for r in self.robots.values() if r.type == 'maintenance'])
            },
            'current_metrics': self.metrics.to_dict() if self.metrics else None,
            'ai_model_trained': self.optimizer.is_trained,
            'metrics_collected': len(self.metrics_history)
        }


# Instancia global
ai_coordinator = AICoordinator()


async def main():
    """Función principal para pruebas"""
    print("🚀 Iniciando AI Coordinator...")
    
    # Crear robots iniciales
    for i in range(50):
        robot_type = np.random.choice(['manufacturing', 'research', 'security', 'maintenance'])
        await ai_coordinator.add_robot(robot_type)
    
    # Iniciar sistema
    try:
        await ai_coordinator.start()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo sistema...")
        await ai_coordinator.stop()


if __name__ == "__main__":
    asyncio.run(main())
