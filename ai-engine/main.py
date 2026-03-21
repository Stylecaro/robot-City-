"""
Sistema de IA Central para Ciudad Robot
Motor neuronal avanzado que coordina todos los robots y sistemas de la ciudad virtual.
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from core.neural_coordinator import NeuralCoordinator
from core.robot_manager import RobotManager
from core.city_optimizer import CityOptimizer
from core.decision_engine import DecisionEngine
from core.quantum_core import QuantumCore
from utils.logger import setup_logger
from utils.database import DatabaseManager
from utils.metrics import (
    PrometheusMiddleware,
    metrics_endpoint,
    ws_connections_total,
    ws_active_connections,
    active_robots,
    system_health as system_health_gauge,
    cpu_usage as cpu_usage_gauge,
    memory_usage as memory_usage_gauge,
    robot_commands_total,
    decisions_total,
    neural_inference_duration,
)

# Routers API
from routes.metaverse_endpoints import router as metaverse_router
from routes.economy_endpoints import router as economy_router
from routes.shop_endpoints import router as shop_router
from routes.finance_endpoints import router as finance_router
from routes.security_endpoints import router as security_router
from routes.prison_endpoints import router as prison_router
from routes.pqc_endpoints import router as pqc_router

# Configuración de logging
logger = setup_logger("ai_engine")

@dataclass
class AIStatus:
    """Estado del sistema de IA"""
    active_robots: int
    processing_tasks: int
    system_health: float
    cpu_usage: float
    memory_usage: float
    last_update: str

class AIEngine:
    """Motor principal de IA para Ciudad Robot"""
    
    def __init__(self):
        self.app = FastAPI(title="Ciudad Robot AI Engine", version="1.0.0")
        self.setup_cors()
        self.setup_routes()
        
        # Componentes del sistema
        self.neural_coordinator = NeuralCoordinator()
        self.robot_manager = RobotManager()
        self.city_optimizer = CityOptimizer()
        self.decision_engine = DecisionEngine()
        self.quantum_core = QuantumCore()
        self.db_manager = DatabaseManager()
        
        # Estado del sistema
        self.active_connections: List[WebSocket] = []
        self.system_status = AIStatus(
            active_robots=0,
            processing_tasks=0,
            system_health=100.0,
            cpu_usage=0.0,
            memory_usage=0.0,
            last_update=datetime.now().isoformat()
        )
        
        logger.info("AI Engine iniciado correctamente")
    
    def setup_cors(self):
        """Configurar CORS para permitir conexiones del frontend"""
        self.app.add_middleware(PrometheusMiddleware)
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000", "http://localhost:8080"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """Configurar rutas de la API"""

        # Routers de sistemas
        self.app.include_router(metaverse_router)
        self.app.include_router(economy_router)
        self.app.include_router(shop_router)
        self.app.include_router(finance_router)
        self.app.include_router(security_router)
        self.app.include_router(prison_router)
        self.app.include_router(pqc_router)

        @self.app.get("/metrics")
        async def prometheus_metrics():
            return metrics_endpoint()

        @self.app.get("/")
        async def root():
            return {"message": "Ciudad Robot AI Engine", "status": "active"}
        
        @self.app.get("/status")
        async def get_status():
            """Obtener estado actual del sistema"""
            await self.update_system_status()
            return asdict(self.system_status)
        
        @self.app.get("/robots")
        async def get_robots():
            """Obtener lista de robots activos"""
            return await self.robot_manager.get_all_robots()
        
        @self.app.post("/robots/create")
        async def create_robot(robot_config: dict):
            """Crear un nuevo robot"""
            robot = await self.robot_manager.create_robot(robot_config)
            await self.notify_clients("robot_created", robot)
            return robot
        
        @self.app.post("/robots/{robot_id}/command")
        async def send_command(robot_id: str, command: dict):
            """Enviar comando a un robot específico"""
            result = await self.robot_manager.send_command(robot_id, command)
            await self.notify_clients("robot_command", {
                "robot_id": robot_id,
                "command": command,
                "result": result
            })
            return result
        
        @self.app.get("/city/optimization")
        async def get_city_optimization():
            """Obtener datos de optimización de la ciudad"""
            return await self.city_optimizer.get_optimization_data()
        
        @self.app.post("/city/optimize")
        async def optimize_city():
            """Ejecutar optimización de la ciudad"""
            result = await self.city_optimizer.optimize()
            await self.notify_clients("city_optimized", result)
            return result

        @self.app.get("/quantum/nodes")
        async def get_quantum_nodes():
            """Listar nodos cuánticos registrados"""
            return {
                "central_city_node_id": self.quantum_core.central_city_node_id,
                "nodes": self.quantum_core.list_nodes()
            }

        @self.app.post("/quantum/nodes/register")
        async def register_quantum_node(payload: dict):
            """Registrar un nodo cuántico nuevo"""
            name = payload.get("name", "Quantum Node")
            location = payload.get("location", "unknown")
            node = self.quantum_core.register_node(name=name, location=location)
            return node.to_dict()

        @self.app.get("/quantum/channels")
        async def get_quantum_channels():
            """Listar canales de entrelazamiento"""
            return self.quantum_core.list_channels()

        @self.app.post("/quantum/entangle")
        async def create_entangled_channel(payload: dict):
            """Crear un canal de entrelazamiento"""
            node_a = payload.get("node_a")
            node_b = payload.get("node_b")
            fidelity = float(payload.get("fidelity", 0.98))
            channel = self.quantum_core.create_entangled_channel(node_a, node_b, fidelity)
            return channel.to_dict()

        @self.app.post("/quantum/transmit")
        async def transmit_quantum_message(payload: dict):
            """Transmitir mensaje por canal cuántico"""
            channel_id = payload.get("channel_id")
            message = payload.get("message", "")
            noise = float(payload.get("noise", 0.01))
            return self.quantum_core.transmit(channel_id, message, noise)
        
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket para comunicación en tiempo real"""
            await self.connect_websocket(websocket)
    
    async def connect_websocket(self, websocket: WebSocket):
        """Manejar nueva conexión WebSocket"""
        await websocket.accept()
        self.active_connections.append(websocket)
        ws_connections_total.inc()
        ws_active_connections.inc()
        
        try:
            # Enviar estado inicial
            await websocket.send_json({
                "type": "status",
                "data": asdict(self.system_status)
            })
            
            # Escuchar mensajes del cliente
            while True:
                data = await websocket.receive_json()
                await self.handle_websocket_message(websocket, data)
                
        except WebSocketDisconnect:
            self.active_connections.remove(websocket)
            ws_active_connections.dec()
            logger.info("Cliente WebSocket desconectado")
        except Exception as e:
            logger.error(f"Error en WebSocket: {e}")
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
    
    async def handle_websocket_message(self, websocket: WebSocket, data: dict):
        """Procesar mensaje recibido por WebSocket"""
        message_type = data.get("type")
        payload = data.get("data", {})
        
        if message_type == "get_robots":
            robots = await self.robot_manager.get_all_robots()
            await websocket.send_json({
                "type": "robots_data",
                "data": robots
            })
        
        elif message_type == "ai_decision":
            decision = await self.decision_engine.make_decision(payload)
            await websocket.send_json({
                "type": "ai_decision_result",
                "data": decision
            })
        
        elif message_type == "neural_analysis":
            analysis = await self.neural_coordinator.analyze(payload)
            await websocket.send_json({
                "type": "neural_analysis_result",
                "data": analysis
            })

        elif message_type == "quantum_message":
            channel_id = payload.get("channel_id")
            message = payload.get("message", "")
            noise = float(payload.get("noise", 0.01))
            result = self.quantum_core.transmit(channel_id, message, noise)
            await websocket.send_json({
                "type": "quantum_message_result",
                "data": result
            })
    
    async def notify_clients(self, event_type: str, data: Any):
        """Notificar a todos los clientes conectados"""
        if not self.active_connections:
            return
        
        message = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Enviar a todos los clientes conectados
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                disconnected.append(connection)
        
        # Remover conexiones muertas
        for connection in disconnected:
            self.active_connections.remove(connection)
    
    async def update_system_status(self):
        """Actualizar estado del sistema"""
        import psutil
        
        self.system_status.active_robots = await self.robot_manager.get_robot_count()
        self.system_status.processing_tasks = await self.get_processing_tasks()
        self.system_status.cpu_usage = psutil.cpu_percent()
        self.system_status.memory_usage = psutil.virtual_memory().percent
        self.system_status.system_health = await self.calculate_system_health()
        self.system_status.last_update = datetime.now().isoformat()

        # Actualizar gauges Prometheus
        active_robots.set(self.system_status.active_robots)
        system_health_gauge.set(self.system_status.system_health)
        cpu_usage_gauge.set(self.system_status.cpu_usage)
        memory_usage_gauge.set(self.system_status.memory_usage)
    
    async def get_processing_tasks(self) -> int:
        """Obtener número de tareas en procesamiento"""
        # Implementar lógica para contar tareas activas
        return 0
    
    async def calculate_system_health(self) -> float:
        """Calcular salud general del sistema"""
        # Implementar algoritmo de salud del sistema
        health_factors = [
            100 - self.system_status.cpu_usage,
            100 - self.system_status.memory_usage,
            90.0 if self.system_status.active_robots > 0 else 70.0
        ]
        return sum(health_factors) / len(health_factors)
    
    async def start_background_tasks(self):
        """Iniciar tareas en segundo plano"""
        asyncio.create_task(self.periodic_status_update())
        asyncio.create_task(self.neural_coordinator.start_processing())
        asyncio.create_task(self.city_optimizer.start_monitoring())
    
    async def periodic_status_update(self):
        """Actualización periódica del estado"""
        while True:
            await asyncio.sleep(5)  # Actualizar cada 5 segundos
            await self.update_system_status()
            await self.notify_clients("status_update", asdict(self.system_status))

# Instancia global del motor de IA
ai_engine = AIEngine()

async def startup_event():
    """Eventos de inicio"""
    logger.info("Iniciando tareas de fondo...")
    await ai_engine.start_background_tasks()

# Configurar eventos de FastAPI
ai_engine.app.add_event_handler("startup", startup_event)

if __name__ == "__main__":
    logger.info("Iniciando Ciudad Robot AI Engine...")
    uvicorn.run(
        "main:ai_engine.app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )