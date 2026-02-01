"""
Metaverso Server Simple - Servidor Funcional sin Dependencias Complejas
"""
import sys
import os
import asyncio
import json
import logging
from datetime import datetime
from typing import Set, Dict, Any
import webbrowser
import time

try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.responses import HTMLResponse
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("⚠️  FastAPI no disponible - instalando...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "websockets"])
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.responses import HTMLResponse
    import uvicorn
    FASTAPI_AVAILABLE = True

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class SimpleMetaversoServer:
    """Servidor simple del metaverso"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8765):
        self.host = host
        self.port = port
        self.app = FastAPI(title="Metaverso Ciudad Robot")
        
        self.unity_clients: Set[WebSocket] = set()
        self.web_clients: Set[WebSocket] = set()
        
        self.robots = {}
        self.robot_count = 0
        self.system_active = True
        
        self._setup_routes()
        logger.info("✅ Servidor inicializado")
    
    def _setup_routes(self):
        """Configura rutas"""
        
        @self.app.get("/")
        async def root():
            return HTMLResponse(self._get_dashboard_html())
        
        @self.app.get("/api/status")
        async def get_status():
            return {
                "system_active": self.system_active,
                "total_robots": len(self.robots),
                "active_robots": sum(1 for r in self.robots.values() if r.get("state") == "working"),
                "unity_clients": len(self.unity_clients),
                "web_clients": len(self.web_clients),
                "timestamp": datetime.now().isoformat()
            }
        
        @self.app.get("/api/robots")
        async def get_robots():
            return {
                "total": len(self.robots),
                "robots": list(self.robots.values())
            }
        
        @self.app.post("/api/spawn_robot")
        async def spawn_robot(robot_type: str = "manufacturing"):
            robot_id = f"{robot_type}_{self.robot_count}"
            self.robot_count += 1
            
            robot = {
                "robot_id": robot_id,
                "robot_type": robot_type,
                "state": "idle",
                "battery_level": 1.0,
                "health": 1.0,
                "position": [0, 0, 0],
                "tasks_completed": 0
            }
            
            self.robots[robot_id] = robot
            logger.info(f"🤖 Robot creado: {robot_id}")
            
            # Broadcast a clientes Unity
            await self._broadcast_to_unity({
                "type": "spawn_robot",
                "robot": robot
            })
            
            return robot
        
        @self.app.websocket("/ws/unity")
        async def unity_websocket(websocket: WebSocket):
            await websocket.accept()
            self.unity_clients.add(websocket)
            logger.info(f"🎮 Cliente Unity conectado ({len(self.unity_clients)} total)")
            
            try:
                while True:
                    data = await websocket.receive_json()
                    await self._handle_unity_message(data)
            except WebSocketDisconnect:
                self.unity_clients.remove(websocket)
                logger.info(f"🎮 Cliente Unity desconectado")
        
        @self.app.websocket("/ws/web")
        async def web_websocket(websocket: WebSocket):
            await websocket.accept()
            self.web_clients.add(websocket)
            logger.info(f"🌐 Cliente web conectado ({len(self.web_clients)} total)")
            
            try:
                while True:
                    data = await websocket.receive_json()
                    
                    if data.get("type") == "spawn_robot":
                        robot_type = data.get("robot_type", "manufacturing")
                        robot = await spawn_robot(robot_type)
                        await websocket.send_json({"type": "robot_spawned", "robot": robot})
                    
            except WebSocketDisconnect:
                self.web_clients.remove(websocket)
                logger.info(f"🌐 Cliente web desconectado")
    
    async def _handle_unity_message(self, data: Dict):
        """Procesa mensajes de Unity"""
        msg_type = data.get("type")
        
        if msg_type == "city_status":
            logger.info(f"📊 Unity reporta: {data.get('total_robots', 0)} robots")
        elif msg_type == "robot_update":
            robot_id = data.get("robot_id")
            if robot_id in self.robots:
                self.robots[robot_id].update(data)
    
    async def _broadcast_to_unity(self, message: Dict):
        """Broadcast a Unity"""
        disconnected = set()
        for client in self.unity_clients:
            try:
                await client.send_json(message)
            except:
                disconnected.add(client)
        self.unity_clients -= disconnected
    
    async def _broadcast_to_web(self, message: Dict):
        """Broadcast a web"""
        disconnected = set()
        for client in self.web_clients:
            try:
                await client.send_json(message)
            except:
                disconnected.add(client)
        self.web_clients -= disconnected
    
    def _get_dashboard_html(self) -> str:
        """HTML del dashboard"""
        return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Metaverso Ciudad Robot</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .status {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
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
            font-size: 1.3em;
            color: #00ff88;
        }
        button {
            background: linear-gradient(135deg, #00ff88, #00ccff);
            border: none;
            color: white;
            padding: 15px 30px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: bold;
            margin: 10px;
            transition: transform 0.2s;
        }
        button:hover { transform: scale(1.05); }
        button:active { transform: scale(0.95); }
        .controls { text-align: center; margin: 20px 0; }
        #connectionStatus {
            text-align: center;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 1.2em;
        }
        .robot-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .robot-card {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            border-left: 4px solid #00ff88;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Metaverso Ciudad Robot</h1>
        
        <div id="connectionStatus" style="background: rgba(255,0,0,0.3);">
            🔴 Desconectado
        </div>
        
        <div class="status">
            <h2>📊 Estado del Sistema</h2>
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
        
        <div class="controls">
            <button onclick="spawnRobot('manufacturing')">➕ Robot Manufactura</button>
            <button onclick="spawnRobot('research')">➕ Robot Investigación</button>
            <button onclick="spawnRobot('security')">➕ Robot Seguridad</button>
            <button onclick="refreshData()">🔄 Actualizar</button>
        </div>
        
        <div class="status">
            <h2>🤖 Robots en el Sistema</h2>
            <div class="robot-list" id="robotList">
                <p style="opacity: 0.6; text-align: center;">No hay robots aún</p>
            </div>
        </div>
    </div>
    
    <script>
        let ws = null;
        
        function connect() {
            ws = new WebSocket(`ws://${window.location.host}/ws/web`);
            
            ws.onopen = () => {
                console.log('✅ Conectado');
                document.getElementById('connectionStatus').innerHTML = '🟢 Conectado';
                document.getElementById('connectionStatus').style.background = 'rgba(0,255,0,0.3)';
                refreshData();
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('Mensaje:', data);
                if (data.type === 'robot_spawned') {
                    refreshData();
                }
            };
            
            ws.onclose = () => {
                console.log('❌ Desconectado');
                document.getElementById('connectionStatus').innerHTML = '🔴 Desconectado';
                document.getElementById('connectionStatus').style.background = 'rgba(255,0,0,0.3)';
                setTimeout(connect, 3000);
            };
        }
        
        async function refreshData() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                document.getElementById('totalRobots').textContent = data.total_robots || 0;
                document.getElementById('activeRobots').textContent = data.active_robots || 0;
                document.getElementById('unityClients').textContent = data.unity_clients || 0;
                
                // Actualizar lista de robots
                const robotsResponse = await fetch('/api/robots');
                const robotsData = await robotsResponse.json();
                
                const robotList = document.getElementById('robotList');
                if (robotsData.robots.length === 0) {
                    robotList.innerHTML = '<p style="opacity: 0.6; text-align: center;">No hay robots aún</p>';
                } else {
                    robotList.innerHTML = robotsData.robots.map(robot => `
                        <div class="robot-card">
                            <strong>${robot.robot_id}</strong><br>
                            Tipo: ${robot.robot_type}<br>
                            Estado: ${robot.state}<br>
                            Batería: ${(robot.battery_level * 100).toFixed(0)}%
                        </div>
                    `).join('');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
        
        function spawnRobot(type) {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'spawn_robot',
                    robot_type: type
                }));
            } else {
                fetch('/api/spawn_robot?robot_type=' + type, { method: 'POST' })
                    .then(() => setTimeout(refreshData, 500));
            }
        }
        
        connect();
        setInterval(refreshData, 3000);
    </script>
</body>
</html>
        """
    
    async def start(self):
        """Inicia el servidor"""
        logger.info("🚀 Iniciando servidor...")
        
        # Crear algunos robots iniciales
        for i in range(5):
            robot_type = ['manufacturing', 'research', 'security'][i % 3]
            await spawn_robot(robot_type)
        
        logger.info(f"✅ Servidor listo en http://{self.host}:{self.port}")
        logger.info("📍 Dashboard: http://localhost:8765")
        logger.info("📍 API: http://localhost:8765/api/status")
        
        # Abrir navegador
        time.sleep(1)
        try:
            webbrowser.open(f"http://localhost:{self.port}")
        except:
            pass
        
        config = uvicorn.Config(self.app, host=self.host, port=self.port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()


async def spawn_robot(robot_type: str):
    """Helper para crear robot"""
    return {"robot_id": f"{robot_type}_temp", "robot_type": robot_type}


# Instancia global
server = SimpleMetaversoServer()


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🤖 METAVERSO CIUDAD ROBOT - SERVIDOR SIMPLE 🌟      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    asyncio.run(server.start())
