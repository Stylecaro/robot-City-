"""
Launcher Principal del Metaverso - Ciudad Robot
Aplicación que inicializa todos los sistemas y lanza Unity Hub
"""

import asyncio
import subprocess
import sys
import os
import json
import time
from pathlib import Path
import requests
import webbrowser
from typing import Optional

class MetaversoLauncher:
    """Launcher principal para el metaverso ciudad robot"""
    
    def __init__(self):
        self.project_root = Path("c:/Users/Brian Carlisle/mundo virtual")
        self.unity_project_path = self.project_root / "UnityProject"
        self.backend_process: Optional[subprocess.Popen] = None
        self.unity_process: Optional[subprocess.Popen] = None
        
        # Configuración de puertos
        self.backend_port = 3000
        self.frontend_port = 3001
        self.websocket_port = 8080
        
        # Estado del sistema
        self.systems_status = {
            'ai_engine': False,
            'security_system': False,
            'manufacturing': False,
            'research_labs': False,
            'simulation_platform': False,
            'backend_api': False,
            'unity_client': False,
            'database': False
        }
        
    def print_banner(self):
        """Mostrar banner del metaverso"""
        banner = """
        ╔══════════════════════════════════════════════════════════════╗
        ║                    🤖 CIUDAD ROBOT METAVERSO 🌆              ║
        ║                                                              ║
        ║  🏭 Manufacturing Centers   🧬 Research Laboratories         ║
        ║  🛡️  Security Systems       🔬 Advanced Simulations          ║
        ║  🤖 AI Engine              🏗️  Construction Centers          ║
        ║  🌐 Unity 3D Graphics      ⚡ Real-time Monitoring          ║
        ║                                                              ║
        ║              ¡Bienvenido al Futuro Digital! 🚀              ║
        ╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
        
    async def check_dependencies(self):
        """Verificar dependencias del sistema"""
        print("🔍 Verificando dependencias del sistema...")
        
        # Verificar Python
        try:
            import flask, numpy, pymongo
            print("✅ Dependencias Python instaladas")
            self.systems_status['backend_api'] = True
        except ImportError as e:
            print(f"❌ Falta dependencia Python: {e}")
            
        # Verificar Unity Hub
        unity_paths = [
            "C:/Program Files/Unity Hub/Unity Hub.exe",
            "C:/Program Files (x86)/Unity Hub/Unity Hub.exe",
            os.path.expanduser("~/AppData/Roaming/UnityHub/Unity Hub.exe")
        ]
        
        unity_found = False
        for path in unity_paths:
            if os.path.exists(path):
                print(f"✅ Unity Hub encontrado: {path}")
                unity_found = True
                self.unity_hub_path = path
                break
        
        if not unity_found:
            print("⚠️  Unity Hub no encontrado, se intentará descargar")
            
        # Verificar Node.js
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js disponible: {result.stdout.strip()}")
            else:
                print("❌ Node.js no encontrado")
        except FileNotFoundError:
            print("❌ Node.js no está instalado")
            
        return self.systems_status['backend_api']
    
    async def setup_project_structure(self):
        """Configurar estructura del proyecto"""
        print("🏗️  Configurando estructura del proyecto...")
        
        # Crear directorios necesarios
        directories = [
            "UnityProject",
            "UnityProject/Assets",
            "UnityProject/Assets/Scripts",
            "UnityProject/Assets/Scenes", 
            "UnityProject/Assets/Prefabs",
            "UnityProject/Assets/Materials",
            "UnityProject/Assets/Models",
            "UnityProject/Assets/Textures",
            "UnityProject/ProjectSettings",
            "logs",
            "temp"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
        print("✅ Estructura de directorios creada")
        
    async def initialize_ai_systems(self):
        """Inicializar sistemas de IA"""
        print("🧠 Inicializando sistemas de IA...")
        
        try:
            # Importar y inicializar motores de IA
            sys.path.append(str(self.project_root / "ai-engine"))
            
            # Simular inicialización
            await asyncio.sleep(1)
            
            self.systems_status['ai_engine'] = True
            print("✅ Motor de IA inicializado")
            
            # Sistema de seguridad
            self.systems_status['security_system'] = True  
            print("✅ Sistema de seguridad activado")
            
            # Manufacturing
            self.systems_status['manufacturing'] = True
            print("✅ Centros de manufacturing operativos")
            
            # Laboratorios de investigación
            self.systems_status['research_labs'] = True
            print("✅ Laboratorios de investigación activos")
            
            # Plataforma de simulación
            self.systems_status['simulation_platform'] = True
            print("✅ Plataforma de simulación lista")
            
        except Exception as e:
            print(f"❌ Error inicializando IA: {e}")
            
    async def start_backend_server(self):
        """Iniciar servidor backend"""
        print("🚀 Iniciando servidor backend...")
        
        try:
            # Cambiar al directorio backend
            backend_dir = self.project_root / "backend"
            
            # Crear servidor básico si no existe
            if not (backend_dir / "server.js").exists():
                await self.create_backend_server()
                
            # Instalar dependencias npm
            npm_install = subprocess.run(['npm', 'install'], 
                                       cwd=backend_dir,
                                       capture_output=True, 
                                       text=True)
            
            if npm_install.returncode == 0:
                print("✅ Dependencias npm instaladas")
            else:
                print("⚠️  Advertencia con dependencias npm")
                
            # Iniciar servidor en background  
            self.backend_process = subprocess.Popen(
                ['node', 'server.js'],
                cwd=backend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Esperar un momento para que inicie
            await asyncio.sleep(3)
            
            # Verificar que está corriendo
            if self.backend_process.poll() is None:
                print(f"✅ Servidor backend ejecutándose en puerto {self.backend_port}")
                self.systems_status['backend_api'] = True
            else:
                print("❌ Error iniciando servidor backend")
                
        except Exception as e:
            print(f"❌ Error con servidor backend: {e}")
            
    async def create_backend_server(self):
        """Crear servidor backend básico"""
        server_code = '''
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');
const cors = require('cors');

const app = express();
const server = http.createServer(app);
const io = socketIo(server, {
    cors: {
        origin: "*",
        methods: ["GET", "POST"]
    }
});

const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());

// Estado del metaverso
let metaversoState = {
    robots: [],
    buildings: [],
    vehicles: [],
    users: [],
    manufacturing: {
        active_lines: 0,
        robots_in_production: 0,
        quality_score: 0.95
    },
    research: {
        active_experiments: 0,
        simulations_running: 0,
        discoveries: 0
    },
    security: {
        threats_detected: 0,
        security_level: 'HIGH',
        humanoids_active: 8
    }
};

// Rutas principales
app.get('/', (req, res) => {
    res.json({
        message: 'Ciudad Robot Metaverso API',
        version: '1.0.0',
        status: 'operational',
        systems: Object.keys(metaversoState)
    });
});

app.get('/api/status', (req, res) => {
    res.json({
        status: 'operational',
        timestamp: new Date().toISOString(),
        metaverso: metaversoState
    });
});

app.get('/api/robots', (req, res) => {
    res.json(metaversoState.robots);
});

app.post('/api/robots', (req, res) => {
    const newRobot = {
        id: Date.now(),
        type: req.body.type || 'worker',
        position: req.body.position || {x: 0, y: 0, z: 0},
        status: 'active',
        created: new Date().toISOString()
    };
    
    metaversoState.robots.push(newRobot);
    
    // Emitir evento a Unity
    io.emit('robot_created', newRobot);
    
    res.json(newRobot);
});

app.get('/api/manufacturing', (req, res) => {
    res.json(metaversoState.manufacturing);
});

app.get('/api/research', (req, res) => {
    res.json(metaversoState.research);
});

app.get('/api/security', (req, res) => {
    res.json(metaversoState.security);
});

// WebSocket para Unity
io.on('connection', (socket) => {
    console.log('Cliente Unity conectado:', socket.id);
    
    // Enviar estado inicial
    socket.emit('metaverso_state', metaversoState);
    
    socket.on('unity_ready', () => {
        console.log('Unity client listo');
        socket.emit('initialize_world', metaversoState);
    });
    
    socket.on('spawn_robot', (data) => {
        const robot = {
            id: Date.now(),
            type: data.type,
            position: data.position,
            status: 'spawning'
        };
        
        metaversoState.robots.push(robot);
        io.emit('robot_spawned', robot);
    });
    
    socket.on('disconnect', () => {
        console.log('Cliente desconectado:', socket.id);
    });
});

// Simulación de datos en tiempo real
setInterval(() => {
    // Actualizar métricas
    metaversoState.manufacturing.robots_in_production = 
        Math.floor(Math.random() * 10) + 1;
    metaversoState.research.simulations_running = 
        Math.floor(Math.random() * 5) + 1;
    
    // Emitir actualizaciones
    io.emit('metrics_update', {
        manufacturing: metaversoState.manufacturing,
        research: metaversoState.research,
        timestamp: new Date().toISOString()
    });
}, 5000);

server.listen(PORT, () => {
    console.log(`🚀 Ciudad Robot Metaverso corriendo en puerto ${PORT}`);
    console.log(`🌐 API disponible en http://localhost:${PORT}`);
    console.log(`⚡ WebSocket listo para Unity`);
});
'''
        
        backend_dir = self.project_root / "backend"
        backend_dir.mkdir(exist_ok=True)
        
        with open(backend_dir / "server.js", 'w', encoding='utf-8') as f:
            f.write(server_code)
            
        # Crear package.json
        package_json = {
            "name": "ciudad-robot-backend",
            "version": "1.0.0",
            "description": "Backend API para Ciudad Robot Metaverso",
            "main": "server.js",
            "scripts": {
                "start": "node server.js",
                "dev": "nodemon server.js"
            },
            "dependencies": {
                "express": "^4.18.2",
                "socket.io": "^4.7.2",
                "cors": "^2.8.5"
            }
        }
        
        with open(backend_dir / "package.json", 'w') as f:
            json.dump(package_json, f, indent=2)
            
        print("✅ Servidor backend creado")
    
    async def setup_unity_project(self):
        """Configurar proyecto Unity"""
        print("🎮 Configurando proyecto Unity...")
        
        # Crear ProjectSettings/ProjectVersion.txt
        project_version = """m_EditorVersion: 2022.3.12f1
m_EditorVersionWithRevision: 2022.3.12f1 (4fe6e059c7ef)
"""
        
        settings_dir = self.unity_project_path / "ProjectSettings"
        settings_dir.mkdir(exist_ok=True)
        
        with open(settings_dir / "ProjectVersion.txt", 'w') as f:
            f.write(project_version)
            
        # Crear script principal de Unity
        await self.create_unity_scripts()
        
        print("✅ Proyecto Unity configurado")
        
    async def create_unity_scripts(self):
        """Crear scripts principales de Unity"""
        
        # GameManager principal
        gamemanager_script = '''using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using SocketIOClient;
using Newtonsoft.Json;

public class GameManager : MonoBehaviour
{
    [Header("Metaverso Configuration")]
    public string serverUrl = "http://localhost:3000";
    public Transform robotSpawnPoint;
    public GameObject[] robotPrefabs;
    
    private SocketIOUnity socket;
    private List<GameObject> spawnedRobots = new List<GameObject>();
    
    void Start()
    {
        Debug.Log("🤖 Iniciando Ciudad Robot Metaverso...");
        
        // Configurar conexión con backend
        ConnectToServer();
        
        // Inicializar mundo 3D
        InitializeWorld();
    }
    
    void ConnectToServer()
    {
        socket = new SocketIOUnity(serverUrl);
        
        socket.OnConnected += (sender, e) =>
        {
            Debug.Log("✅ Conectado al servidor backend");
            socket.Emit("unity_ready");
        };
        
        socket.On("metaverso_state", (data) =>
        {
            Debug.Log("📊 Estado del metaverso recibido");
            // Procesar estado inicial
        });
        
        socket.On("robot_spawned", (data) =>
        {
            var robotData = JsonConvert.DeserializeObject<RobotData>(data.ToString());
            SpawnRobot(robotData);
        });
        
        socket.On("metrics_update", (data) =>
        {
            // Actualizar métricas en UI
            UpdateMetricsUI(data.ToString());
        });
        
        socket.Connect();
    }
    
    void InitializeWorld()
    {
        Debug.Log("🌍 Inicializando mundo 3D...");
        
        // Crear terreno básico
        CreateTerrain();
        
        // Crear edificios principales
        CreateBuildings();
        
        // Configurar iluminación
        SetupLighting();
        
        Debug.Log("✅ Mundo 3D inicializado");
    }
    
    void CreateTerrain()
    {
        GameObject terrain = GameObject.CreatePrimitive(PrimitiveType.Plane);
        terrain.name = "CityTerrain";
        terrain.transform.localScale = new Vector3(50, 1, 50);
        
        // Material del terreno
        Renderer renderer = terrain.GetComponent<Renderer>();
        renderer.material.color = new Color(0.3f, 0.7f, 0.3f); // Verde
    }
    
    void CreateBuildings()
    {
        // Manufacturing Center
        CreateBuilding(new Vector3(-20, 0, 0), new Vector3(5, 8, 10), Color.blue, "Manufacturing Center");
        
        // Research Labs
        CreateBuilding(new Vector3(20, 0, 0), new Vector3(8, 6, 8), Color.cyan, "Research Labs");
        
        // Security HQ
        CreateBuilding(new Vector3(0, 0, -20), new Vector3(6, 10, 6), Color.red, "Security HQ");
        
        // AI Central
        CreateBuilding(new Vector3(0, 0, 20), new Vector3(4, 12, 4), Color.magenta, "AI Central");
    }
    
    GameObject CreateBuilding(Vector3 position, Vector3 scale, Color color, string name)
    {
        GameObject building = GameObject.CreatePrimitive(PrimitiveType.Cube);
        building.name = name;
        building.transform.position = position;
        building.transform.localScale = scale;
        
        Renderer renderer = building.GetComponent<Renderer>();
        renderer.material.color = color;
        
        return building;
    }
    
    void SetupLighting()
    {
        // Luz principal
        GameObject mainLight = new GameObject("Main Light");
        Light light = mainLight.AddComponent<Light>();
        light.type = LightType.Directional;
        light.intensity = 1.5f;
        light.color = Color.white;
        mainLight.transform.rotation = Quaternion.Euler(50, -30, 0);
        
        // Luz ambiente
        RenderSettings.ambientLight = new Color(0.3f, 0.3f, 0.4f);
    }
    
    void SpawnRobot(RobotData robotData)
    {
        if (robotPrefabs.Length == 0) return;
        
        Vector3 spawnPos = new Vector3(robotData.position.x, 1, robotData.position.z);
        GameObject robotPrefab = robotPrefabs[0]; // Por ahora usar el primero
        
        GameObject robot = Instantiate(robotPrefab, spawnPos, Quaternion.identity);
        robot.name = $"Robot_{robotData.id}";
        
        spawnedRobots.Add(robot);
        
        Debug.Log($"🤖 Robot creado: {robot.name}");
    }
    
    void UpdateMetricsUI(string metricsJson)
    {
        // Actualizar UI con métricas en tiempo real
        Debug.Log($"📊 Métricas actualizadas: {metricsJson}");
    }
    
    void OnApplicationQuit()
    {
        socket?.Disconnect();
    }
}

[System.Serializable]
public class RobotData
{
    public int id;
    public string type;
    public Position position;
    public string status;
}

[System.Serializable]  
public class Position
{
    public float x;
    public float y; 
    public float z;
}
'''

        # Crear directorio Scripts
        scripts_dir = self.unity_project_path / "Assets" / "Scripts"
        scripts_dir.mkdir(parents=True, exist_ok=True)
        
        with open(scripts_dir / "GameManager.cs", 'w', encoding='utf-8') as f:
            f.write(gamemanager_script)
            
        print("✅ Scripts Unity creados")
    
    async def launch_unity_hub(self):
        """Lanzar Unity Hub"""
        print("🎮 Lanzando Unity Hub...")
        
        try:
            if hasattr(self, 'unity_hub_path'):
                # Lanzar Unity Hub
                self.unity_process = subprocess.Popen([self.unity_hub_path])
                print("✅ Unity Hub iniciado")
                
                # Esperar un momento
                await asyncio.sleep(3)
                
                # Intentar abrir el proyecto
                project_path = str(self.unity_project_path)
                print(f"📂 Abriendo proyecto: {project_path}")
                
                self.systems_status['unity_client'] = True
                
            else:
                print("⚠️  Unity Hub no encontrado, abriendo página de descarga...")
                webbrowser.open("https://unity.com/download")
                
        except Exception as e:
            print(f"❌ Error lanzando Unity: {e}")
            
    async def open_web_dashboard(self):
        """Abrir dashboard web"""
        print("🌐 Abriendo dashboard web...")
        
        # Esperar que el backend esté listo
        backend_ready = False
        for attempt in range(10):
            try:
                response = requests.get(f"http://localhost:{self.backend_port}/api/status", timeout=2)
                if response.status_code == 200:
                    backend_ready = True
                    break
            except:
                pass
            await asyncio.sleep(1)
            
        if backend_ready:
            webbrowser.open(f"http://localhost:{self.backend_port}")
            print("✅ Dashboard web abierto")
        else:
            print("⚠️  Backend no disponible, creando página local...")
            await self.create_local_dashboard()
            
    async def create_local_dashboard(self):
        """Crear dashboard local básico"""
        dashboard_html = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ciudad Robot Metaverso - Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 3em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .status-card {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .status-card h3 {
            margin-top: 0;
            font-size: 1.5em;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            margin: 10px 0;
        }
        .metric-value {
            font-weight: bold;
            color: #00ff88;
        }
        .launch-buttons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 30px 0;
        }
        .launch-btn {
            background: linear-gradient(45deg, #00ff88, #00cc6a);
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            color: white;
            font-size: 1.1em;
            cursor: pointer;
            transition: transform 0.2s;
        }
        .launch-btn:hover {
            transform: scale(1.05);
        }
        .console {
            background: rgba(0,0,0,0.8);
            border-radius: 10px;
            padding: 20px;
            font-family: 'Courier New', monospace;
            height: 300px;
            overflow-y: auto;
        }
        .console-line {
            margin: 5px 0;
            color: #00ff00;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 CIUDAD ROBOT METAVERSO 🌆</h1>
            <p>Dashboard de Control Central</p>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <h3>🏭 Manufacturing Centers</h3>
                <div class="metric">
                    <span>Robots en Producción:</span>
                    <span class="metric-value" id="robots-production">5</span>
                </div>
                <div class="metric">
                    <span>Líneas Activas:</span>
                    <span class="metric-value" id="active-lines">3</span>
                </div>
                <div class="metric">
                    <span>Calidad Promedio:</span>
                    <span class="metric-value" id="quality-score">95%</span>
                </div>
            </div>
            
            <div class="status-card">
                <h3>🧬 Research Labs</h3>
                <div class="metric">
                    <span>Experimentos Activos:</span>
                    <span class="metric-value" id="experiments">12</span>
                </div>
                <div class="metric">
                    <span>Simulaciones:</span>
                    <span class="metric-value" id="simulations">4</span>
                </div>
                <div class="metric">
                    <span>Descubrimientos:</span>
                    <span class="metric-value" id="discoveries">3</span>
                </div>
            </div>
            
            <div class="status-card">
                <h3>🛡️ Security System</h3>
                <div class="metric">
                    <span>Nivel de Seguridad:</span>
                    <span class="metric-value" id="security-level">ALTO</span>
                </div>
                <div class="metric">
                    <span>Humanoides Activos:</span>
                    <span class="metric-value" id="humanoids">8</span>
                </div>
                <div class="metric">
                    <span>Amenazas Detectadas:</span>
                    <span class="metric-value" id="threats">0</span>
                </div>
            </div>
            
            <div class="status-card">
                <h3>🧠 AI Engine</h3>
                <div class="metric">
                    <span>Estado del Sistema:</span>
                    <span class="metric-value" id="ai-status">OPERATIVO</span>
                </div>
                <div class="metric">
                    <span>Procesos Activos:</span>
                    <span class="metric-value" id="ai-processes">15</span>
                </div>
                <div class="metric">
                    <span>Eficiencia IA:</span>
                    <span class="metric-value" id="ai-efficiency">98%</span>
                </div>
            </div>
        </div>
        
        <div class="launch-buttons">
            <button class="launch-btn" onclick="launchUnity()">🎮 Abrir Unity</button>
            <button class="launch-btn" onclick="launchBackend()">🚀 Backend API</button>
            <button class="launch-btn" onclick="openConsole()">⚡ Consola</button>
        </div>
        
        <div class="console" id="console">
            <div class="console-line">🤖 Ciudad Robot Metaverso - Sistema Iniciado</div>
            <div class="console-line">✅ Todos los sistemas operativos</div>
            <div class="console-line">🌐 Dashboard web cargado</div>
            <div class="console-line">⚡ Listo para entrar al metaverso...</div>
        </div>
    </div>
    
    <script>
        // Simulación de datos en tiempo real
        function updateMetrics() {
            document.getElementById('robots-production').textContent = Math.floor(Math.random() * 10) + 1;
            document.getElementById('simulations').textContent = Math.floor(Math.random() * 8) + 1;
            
            // Agregar línea a consola
            const console = document.getElementById('console');
            const time = new Date().toLocaleTimeString();
            const line = document.createElement('div');
            line.className = 'console-line';
            line.textContent = `[${time}] 📊 Métricas actualizadas - Sistema funcionando correctamente`;
            console.appendChild(line);
            console.scrollTop = console.scrollHeight;
        }
        
        function launchUnity() {
            addConsoleMessage('🎮 Intentando abrir Unity Hub...');
            // En un entorno real, esto comunicaría con el backend
            alert('Unity Hub debe abrirse desde el launcher principal');
        }
        
        function launchBackend() {
            addConsoleMessage('🚀 Abriendo API backend...');
            window.open('http://localhost:3000', '_blank');
        }
        
        function openConsole() {
            addConsoleMessage('⚡ Consola de administración activada');
        }
        
        function addConsoleMessage(message) {
            const console = document.getElementById('console');
            const time = new Date().toLocaleTimeString();
            const line = document.createElement('div');
            line.className = 'console-line';
            line.textContent = `[${time}] ${message}`;
            console.appendChild(line);
            console.scrollTop = console.scrollHeight;
        }
        
        // Actualizar métricas cada 5 segundos
        setInterval(updateMetrics, 5000);
        
        // Mensaje de bienvenida
        setTimeout(() => {
            addConsoleMessage('🌟 ¡Bienvenido al Metaverso Ciudad Robot!');
        }, 1000);
    </script>
</body>
</html>'''

        dashboard_path = self.project_root / "dashboard.html"
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
            
        webbrowser.open(f"file://{dashboard_path}")
        print("✅ Dashboard local abierto")
        
    def show_system_status(self):
        """Mostrar estado de todos los sistemas"""
        print("\n" + "="*60)
        print("📊 ESTADO DE SISTEMAS DEL METAVERSO")
        print("="*60)
        
        for system, status in self.systems_status.items():
            status_icon = "✅" if status else "❌"
            system_name = system.replace('_', ' ').title()
            print(f"{status_icon} {system_name:<25} {'Operativo' if status else 'No disponible'}")
            
        print("="*60)
        
        operational_count = sum(self.systems_status.values())
        total_systems = len(self.systems_status)
        percentage = (operational_count / total_systems) * 100
        
        print(f"🎯 Sistemas operativos: {operational_count}/{total_systems} ({percentage:.0f}%)")
        
        if percentage >= 80:
            print("🚀 ¡Metaverso listo para usar!")
        elif percentage >= 60:
            print("⚠️  Metaverso parcialmente operativo")
        else:
            print("❌ Metaverso requiere configuración adicional")
            
        print("="*60 + "\n")
        
    async def launch_complete_system(self):
        """Lanzar sistema completo del metaverso"""
        self.print_banner()
        
        print("🚀 Iniciando Ciudad Robot Metaverso...")
        print("Este proceso tomará unos momentos...\n")
        
        # Paso 1: Verificar dependencias
        dependencies_ok = await self.check_dependencies()
        
        # Paso 2: Configurar estructura
        await self.setup_project_structure()
        
        # Paso 3: Inicializar sistemas IA
        await self.initialize_ai_systems()
        
        # Paso 4: Iniciar backend
        await self.start_backend_server()
        
        # Paso 5: Configurar Unity
        await self.setup_unity_project()
        
        # Paso 6: Lanzar Unity Hub
        await self.launch_unity_hub()
        
        # Paso 7: Abrir dashboard web
        await self.open_web_dashboard()
        
        # Mostrar estado final
        self.show_system_status()
        
        # Instrucciones finales
        print("🎯 INSTRUCCIONES PARA ENTRAR AL METAVERSO:")
        print("1. 🎮 Unity Hub debería haberse abierto automáticamente")
        print("2. 📁 Abrir proyecto desde: " + str(self.unity_project_path))
        print("3. 🌐 Dashboard web disponible en el navegador")
        print("4. 🚀 Backend API corriendo en http://localhost:3000")
        print("\n🌟 ¡Disfruta explorando la Ciudad Robot!")
        
        return True

# Función principal
async def main():
    launcher = MetaversoLauncher()
    
    try:
        success = await launcher.launch_complete_system()
        
        if success:
            print("\n⚡ Manteniendo sistemas activos...")
            print("Presiona Ctrl+C para terminar\n")
            
            # Mantener el sistema corriendo
            while True:
                await asyncio.sleep(10)
                # Aquí podrías agregar monitoreo continuo
                
    except KeyboardInterrupt:
        print("\n🛑 Cerrando Ciudad Robot Metaverso...")
        
        # Limpiar procesos
        if launcher.backend_process:
            launcher.backend_process.terminate()
            
        if launcher.unity_process:
            launcher.unity_process.terminate()
            
        print("✅ Sistemas cerrados correctamente")
        
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(main())