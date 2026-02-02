"""
Metaverso Backend Integrado - Servidor Principal con IA
Integra AICoordinator, RobotAI, Predictive Analytics y comunicación en tiempo real
"""
import asyncio
import websockets
import json
import logging
from typing import Set, Dict, Any
from datetime import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Importar sistemas de IA
import sys
import os
sys.path.append(os.path.dirname(__file__))

from ai_engine.core.ai_coordinator import ai_coordinator, CityMetrics
from ai_engine.core.quantum_core import QuantumCore
from ai_engine.core.predictive_analytics import analytics_engine
from robot_system.robot_ai import RobotAI, Position, Task, TaskPriority, create_robot


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MetaversoServer:
    """Servidor principal del metaverso"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self.app = FastAPI(title="Metaverso Ciudad Robot API")
        
        # Conexiones activas
        self.unity_clients: Set[WebSocket] = set()
        self.web_clients: Set[WebSocket] = set()
        
        # Estado del sistema
        self.system_active = False
        self.robots: Dict[str, RobotAI] = {}
        self.quantum_core = QuantumCore()
        
        # Configurar rutas
        self._setup_routes()
        
        logger.info("🚀 Servidor Metaverso inicializado")
    
    def _setup_routes(self):
        """Configura las rutas de la API"""
        
        @self.app.get("/")
        async def root():
            return HTMLResponse(self._get_dashboard_html())
        
        @self.app.get("/api/status")
        async def get_status():
            """Estado del sistema"""
            return {
                "system_active": self.system_active,
                "ai_coordinator": ai_coordinator.get_status(),
                "analytics": analytics_engine.get_stats(),
                "robots": len(self.robots),
                "unity_clients": len(self.unity_clients),
                "web_clients": len(self.web_clients),
                "timestamp": datetime.now().isoformat()
            }
        
        @self.app.get("/api/robots")
        async def get_robots():
            """Lista de todos los robots"""
            return {
                "total": len(self.robots),
                "robots": [r.get_status() for r in self.robots.values()]
            }
        
        @self.app.get("/api/analytics")
        async def get_analytics():
            """Análisis predictivo actual"""
            city_data = {
                "total_robots": len(self.robots),
                "active_robots": len([r for r in self.robots.values() if r.state.value in ['work', 'patrol']]),
                "manufacturing_efficiency": ai_coordinator.metrics.manufacturing_efficiency if ai_coordinator.metrics else 0.0,
                "energy_consumption": ai_coordinator.metrics.energy_consumption if ai_coordinator.metrics else 0.0,
                "robots": [r.get_status() for r in self.robots.values()]
            }
            
            analysis = analytics_engine.analyze_city(city_data)
            return analysis

        @self.app.get("/api/quantum/nodes")
        async def get_quantum_nodes():
            """Lista de nodos cuánticos"""
            return {
                "central_city_node_id": self.quantum_core.central_city_node_id,
                "nodes": self.quantum_core.list_nodes()
            }

        @self.app.post("/api/quantum/nodes/register")
        async def register_quantum_node(payload: Dict):
            """Registrar un nodo cuántico"""
            name = payload.get("name", "Quantum Node")
            location = payload.get("location", "unknown")
            node = self.quantum_core.register_node(name=name, location=location)
            return node.to_dict()

        @self.app.get("/api/quantum/channels")
        async def get_quantum_channels():
            """Lista de canales de entrelazamiento"""
            return self.quantum_core.list_channels()

        @self.app.post("/api/quantum/entangle")
        async def create_quantum_channel(payload: Dict):
            """Crear canal de entrelazamiento"""
            node_a = payload.get("node_a")
            node_b = payload.get("node_b")
            fidelity = float(payload.get("fidelity", 0.98))
            channel = self.quantum_core.create_entangled_channel(node_a, node_b, fidelity)
            return channel.to_dict()

        @self.app.post("/api/quantum/transmit")
        async def transmit_quantum_message(payload: Dict):
            """Transmitir mensaje por canal cuántico"""
            channel_id = payload.get("channel_id")
            message = payload.get("message", "")
            noise = float(payload.get("noise", 0.01))
            return self.quantum_core.transmit(channel_id, message, noise)
        
        @self.app.get("/api/alerts")
        async def get_alerts():
            """Alertas activas"""
            return {
                "total": len(analytics_engine.alerts),
                "alerts": [
                    {
                        "id": a.alert_id,
                        "severity": a.severity,
                        "category": a.category,
                        "message": a.message,
                        "time": a.predicted_time,
                        "action": a.recommended_action,
                        "confidence": a.confidence
                    }
                    for a in analytics_engine.alerts
                ]
            }
        
        @self.app.websocket("/ws/unity")
        async def unity_websocket(websocket: WebSocket):
            """WebSocket para clientes Unity"""
            await websocket.accept()
            self.unity_clients.add(websocket)
            logger.info(f"🎮 Cliente Unity conectado ({len(self.unity_clients)} total)")
            
            try:
                while True:
                    data = await websocket.receive_json()
                    await self._handle_unity_message(data, websocket)
            except WebSocketDisconnect:
                self.unity_clients.remove(websocket)
                logger.info(f"🎮 Cliente Unity desconectado ({len(self.unity_clients)} restantes)")
        
        @self.app.websocket("/ws/web")
        async def web_websocket(websocket: WebSocket):
            """WebSocket para clientes web"""
            await websocket.accept()
            self.web_clients.add(websocket)
            logger.info(f"🌐 Cliente web conectado ({len(self.web_clients)} total)")
            
            try:
                while True:
                    data = await websocket.receive_json()
                    await self._handle_web_message(data, websocket)
            except WebSocketDisconnect:
                self.web_clients.remove(websocket)
                logger.info(f"🌐 Cliente web desconectado ({len(self.web_clients)} restantes)")
    
    async def _handle_unity_message(self, data: Dict, websocket: WebSocket):
        """Procesa mensajes de Unity"""
        msg_type = data.get("type")
        
        if msg_type == "city_status":
            # Actualizar AI Coordinator con datos de Unity
            await self._sync_unity_to_ai(data)
            
        elif msg_type == "robot_update":
            # Actualizar robot específico
            robot_id = data.get("robot_id")
            if robot_id in self.robots:
                # Sincronizar estado
                pass
        
        elif msg_type == "request_command":
            # Unity solicita comando de IA
            response = await self._get_ai_command()
            await websocket.send_json(response)

        elif msg_type == "quantum_message":
            channel_id = data.get("channel_id")
            message = data.get("message", "")
            noise = float(data.get("noise", 0.01))
            result = self.quantum_core.transmit(channel_id, message, noise)
            await websocket.send_json({
                "type": "quantum_message_result",
                "data": result
            })
    
    async def _handle_web_message(self, data: Dict, websocket: WebSocket):
        """Procesa mensajes del dashboard web"""
        msg_type = data.get("type")
        
        if msg_type == "spawn_robot":
            robot_type = data.get("robot_type", "manufacturing")
            robot = await self._create_robot(robot_type)
            
            # Notificar a Unity
            await self._broadcast_to_unity({
                "type": "spawn_robot",
                "robot_data": robot.get_status()
            })
            
        elif msg_type == "assign_task":
            robot_id = data.get("robot_id")
            task_data = data.get("task")
            await self._assign_task(robot_id, task_data)

        elif msg_type == "quantum_entangle":
            node_a = data.get("node_a")
            node_b = data.get("node_b")
            fidelity = float(data.get("fidelity", 0.98))
            channel = self.quantum_core.create_entangled_channel(node_a, node_b, fidelity)
            await websocket.send_json({
                "type": "quantum_entangle_result",
                "data": channel.to_dict()
            })

        elif msg_type == "quantum_message":
            channel_id = data.get("channel_id")
            message = data.get("message", "")
            noise = float(data.get("noise", 0.01))
            result = self.quantum_core.transmit(channel_id, message, noise)
            await websocket.send_json({
                "type": "quantum_message_result",
                "data": result
            })
    
    async def _sync_unity_to_ai(self, data: Dict):
        """Sincroniza datos de Unity con AI Coordinator"""
        # Actualizar métricas
        if ai_coordinator.metrics:
            ai_coordinator.metrics.total_robots = data.get("total_robots", 0)
            ai_coordinator.metrics.active_robots = data.get("active_robots", 0)
            ai_coordinator.metrics.manufacturing_efficiency = data.get("manufacturing_efficiency", 0.0)
    
    async def _get_ai_command(self) -> Dict:
        """Obtiene comando sugerido por IA"""
        if not ai_coordinator.metrics:
            return {"type": "no_command"}
        
        optimizations = ai_coordinator.optimizer.predict_optimization(ai_coordinator.metrics)
        top_action = max(optimizations, key=optimizations.get)
        
        return {
            "type": "ai_command",
            "command": top_action,
            "confidence": optimizations[top_action],
            "all_suggestions": optimizations
        }
    
    async def _create_robot(self, robot_type: str) -> RobotAI:
        """Crea nuevo robot"""
        robot = await create_robot(robot_type)
        self.robots[robot.robot_id] = robot
        
        # Iniciar robot en background
        asyncio.create_task(robot.start())
        
        logger.info(f"🤖 Robot creado: {robot.robot_id}")
        return robot
    
    async def _assign_task(self, robot_id: str, task_data: Dict):
        """Asigna tarea a robot"""
        if robot_id not in self.robots:
            logger.warning(f"Robot {robot_id} no encontrado")
            return
        
        robot = self.robots[robot_id]
        
        task = Task(
            task_id=task_data.get("task_id", f"task_{datetime.now().timestamp()}"),
            task_type=task_data.get("task_type", "general"),
            target_position=Position(
                task_data.get("x", 0),
                task_data.get("y", 0),
                task_data.get("z", 0)
            ),
            priority=TaskPriority[task_data.get("priority", "NORMAL")]
        )
        
        robot.add_task(task)
    
    async def _broadcast_to_unity(self, message: Dict):
        """Envía mensaje a todos los clientes Unity"""
        if not self.unity_clients:
            return
        
        disconnected = set()
        
        for client in self.unity_clients:
            try:
                await client.send_json(message)
            except:
                disconnected.add(client)
        
        # Limpiar desconectados
        self.unity_clients -= disconnected
    
    async def _broadcast_to_web(self, message: Dict):
        """Envía mensaje a todos los clientes web"""
        if not self.web_clients:
            return
        
        disconnected = set()
        
        for client in self.web_clients:
            try:
                await client.send_json(message)
            except:
                disconnected.add(client)
        
        self.web_clients -= disconnected
    
    async def _periodic_sync(self):
        """Sincronización periódica (cada 2 segundos)"""
        while self.system_active:
            try:
                # Obtener estado del AI Coordinator
                ai_status = ai_coordinator.get_status()
                
                # Broadcast a clientes web
                await self._broadcast_to_web({
                    "type": "system_update",
                    "ai_status": ai_status,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Análisis predictivo cada 10 ciclos (20 segundos)
                if datetime.now().second % 20 == 0:
                    city_data = {
                        "total_robots": len(self.robots),
                        "active_robots": len([r for r in self.robots.values() if r.state.value in ['work', 'patrol']]),
                        "robots": [r.get_status() for r in self.robots.values()]
                    }
                    
                    analysis = analytics_engine.analyze_city(city_data)
                    
                    await self._broadcast_to_web({
                        "type": "analytics_update",
                        "analysis": analysis
                    })
                
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error en sincronización periódica: {e}")
                await asyncio.sleep(2)
    
    def _get_dashboard_html(self) -> str:
        """HTML del dashboard de control"""
        return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Metaverso Ciudad Robot - Dashboard IA</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
            animation: fadeIn 1s;
        }
        
        h1 {
            font-size: 3em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            margin-bottom: 10px;
        }
        
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .card {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 40px rgba(0,0,0,0.3);
        }
        
        .card h2 {
            margin-bottom: 15px;
            font-size: 1.5em;
            border-bottom: 2px solid rgba(255,255,255,0.3);
            padding-bottom: 10px;
        }
        
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }
        
        .metric-value {
            font-weight: bold;
            font-size: 1.2em;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        
        .status-active {
            background: #00ff00;
            box-shadow: 0 0 10px #00ff00;
        }
        
        .status-warning {
            background: #ffaa00;
            box-shadow: 0 0 10px #ffaa00;
        }
        
        .status-critical {
            background: #ff0000;
            box-shadow: 0 0 10px #ff0000;
        }
        
        .progress-bar {
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            overflow: hidden;
            height: 20px;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00ff88, #00ccff);
            transition: width 0.5s;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8em;
        }
        
        .alert {
            background: rgba(255,0,0,0.2);
            border-left: 4px solid #ff0000;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }
        
        .recommendation {
            background: rgba(0,255,136,0.2);
            border-left: 4px solid #00ff88;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }
        
        button {
            background: linear-gradient(135deg, #00ff88, #00ccff);
            border: none;
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: transform 0.2s, box-shadow 0.2s;
            margin: 5px;
        }
        
        button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 20px rgba(0,255,136,0.4);
        }
        
        button:active {
            transform: scale(0.95);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .controls {
            text-align: center;
            margin: 20px 0;
        }
        
        #connectionStatus {
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 10px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 Metaverso Ciudad Robot</h1>
            <p>Dashboard de Control con Inteligencia Artificial</p>
        </header>
        
        <div id="connectionStatus" style="background: rgba(255,0,0,0.3);">
            🔴 Desconectado
        </div>
        
        <div class="controls">
            <button onclick="spawnRobot('manufacturing')">➕ Crear Robot Manufactura</button>
            <button onclick="spawnRobot('research')">➕ Crear Robot Investigación</button>
            <button onclick="spawnRobot('security')">➕ Crear Robot Seguridad</button>
            <button onclick="refreshData()">🔄 Actualizar</button>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>🏙️ Estado del Sistema</h2>
                <div class="metric">
                    <span>Estado:</span>
                    <span id="systemStatus">-</span>
                </div>
                <div class="metric">
                    <span>Robots Totales:</span>
                    <span class="metric-value" id="totalRobots">0</span>
                </div>
                <div class="metric">
                    <span>Robots Activos:</span>
                    <span class="metric-value" id="activeRobots">0</span>
                </div>
                <div class="metric">
                    <span>Clientes Unity:</span>
                    <span class="metric-value" id="unityClients">0</span>
                </div>
            </div>
            
            <div class="card">
                <h2>🧠 Inteligencia Artificial</h2>
                <div class="metric">
                    <span>Modelo Entrenado:</span>
                    <span id="aiTrained">-</span>
                </div>
                <div class="metric">
                    <span>Métricas Recopiladas:</span>
                    <span id="metricsCollected">0</span>
                </div>
                <div class="metric">
                    <span>Eficiencia Manufactura:</span>
                    <span id="manufEfficiency">0%</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" id="manufProgress" style="width: 0%">0%</div>
                </div>
            </div>
            
            <div class="card">
                <h2>📊 Análisis Predictivo</h2>
                <div class="metric">
                    <span>Predicción Tráfico:</span>
                    <span id="trafficPred">-</span>
                </div>
                <div class="metric">
                    <span>Predicción Energía:</span>
                    <span id="energyPred">-</span>
                </div>
                <div class="metric">
                    <span>Confianza:</span>
                    <span id="predConfidence">-</span>
                </div>
            </div>
            
            <div class="card">
                <h2>🚨 Alertas Activas</h2>
                <div id="alertsContainer">
                    <p style="opacity: 0.6;">No hay alertas</p>
                </div>
            </div>
            
            <div class="card" style="grid-column: span 2;">
                <h2>💡 Recomendaciones de IA</h2>
                <div id="recommendationsContainer">
                    <p style="opacity: 0.6;">Cargando...</p>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let ws = null;
        
        function connect() {
            ws = new WebSocket(`ws://${window.location.host}/ws/web`);
            
            ws.onopen = () => {
                console.log('✅ Conectado al servidor');
                document.getElementById('connectionStatus').innerHTML = '🟢 Conectado';
                document.getElementById('connectionStatus').style.background = 'rgba(0,255,0,0.3)';
                refreshData();
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleMessage(data);
            };
            
            ws.onclose = () => {
                console.log('❌ Desconectado');
                document.getElementById('connectionStatus').innerHTML = '🔴 Desconectado';
                document.getElementById('connectionStatus').style.background = 'rgba(255,0,0,0.3)';
                setTimeout(connect, 3000);
            };
        }
        
        function handleMessage(data) {
            if (data.type === 'system_update') {
                updateSystemStatus(data.ai_status);
            } else if (data.type === 'analytics_update') {
                updateAnalytics(data.analysis);
            }
        }
        
        function updateSystemStatus(status) {
            document.getElementById('totalRobots').textContent = status.total_robots || 0;
            document.getElementById('activeRobots').textContent = status.robots_by_type?.manufacturing || 0;
            document.getElementById('aiTrained').textContent = status.ai_model_trained ? '✅ Sí' : '⏳ No';
            document.getElementById('metricsCollected').textContent = status.metrics_collected || 0;
            
            if (status.current_metrics) {
                const efficiency = (status.current_metrics.manufacturing_efficiency * 100).toFixed(1);
                document.getElementById('manufEfficiency').textContent = efficiency + '%';
                document.getElementById('manufProgress').style.width = efficiency + '%';
                document.getElementById('manufProgress').textContent = efficiency + '%';
            }
        }
        
        function updateAnalytics(analysis) {
            if (analysis.traffic_prediction) {
                const traffic = (analysis.traffic_prediction.value * 100).toFixed(1);
                document.getElementById('trafficPred').textContent = traffic + '%';
            }
            
            if (analysis.energy_prediction) {
                const energy = (analysis.energy_prediction.value * 100).toFixed(1);
                document.getElementById('energyPred').textContent = energy + '%';
                const confidence = (analysis.energy_prediction.confidence * 100).toFixed(1);
                document.getElementById('predConfidence').textContent = confidence + '%';
            }
            
            // Alertas
            const alertsHTML = analysis.maintenance_alerts.map(alert => `
                <div class="alert">
                    <strong>${alert.severity.toUpperCase()}:</strong> ${alert.message}
                </div>
            `).join('') || '<p style="opacity: 0.6;">No hay alertas</p>';
            document.getElementById('alertsContainer').innerHTML = alertsHTML;
            
            // Recomendaciones
            const recsHTML = analysis.recommendations.map(rec => `
                <div class="recommendation">${rec}</div>
            `).join('');
            document.getElementById('recommendationsContainer').innerHTML = recsHTML;
        }
        
        async function refreshData() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                document.getElementById('systemStatus').innerHTML = data.system_active ? 
                    '<span class="status-indicator status-active"></span>Activo' :
                    '<span class="status-indicator status-warning"></span>Inactivo';
                document.getElementById('unityClients').textContent = data.unity_clients || 0;
                
                updateSystemStatus(data.ai_coordinator);
                
                // Análisis
                const analytics = await fetch('/api/analytics');
                const analysisData = await analytics.json();
                updateAnalytics(analysisData);
            } catch (error) {
                console.error('Error actualizando datos:', error);
            }
        }
        
        function spawnRobot(type) {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'spawn_robot',
                    robot_type: type
                }));
                setTimeout(refreshData, 1000);
            }
        }
        
        // Conectar al iniciar
        connect();
        
        // Auto-actualizar cada 5 segundos
        setInterval(refreshData, 5000);
    </script>
</body>
</html>
        """
    
    async def start(self):
        """Inicia el servidor"""
        self.system_active = True
        
        logger.info("🚀 Iniciando sistemas...")
        
        # Iniciar AI Coordinator
        asyncio.create_task(ai_coordinator.start())
        
        # Crear robots iniciales
        for i in range(10):
            robot_type = ['manufacturing', 'research', 'security', 'maintenance'][i % 4]
            await self._create_robot(robot_type)
        
        # Iniciar sincronización periódica
        asyncio.create_task(self._periodic_sync())
        
        # Iniciar servidor FastAPI
        config = uvicorn.Config(self.app, host=self.host, port=self.port, log_level="info")
        server = uvicorn.Server(config)
        
        logger.info(f"✅ Servidor corriendo en http://{self.host}:{self.port}")
        await server.serve()


# Instancia global
server = MetaversoServer()


if __name__ == "__main__":
    asyncio.run(server.start())
