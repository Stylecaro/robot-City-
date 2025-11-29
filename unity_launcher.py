"""
Unity Integration Launcher
Configuración y lanzamiento de Unity Hub para gráficos avanzados del metaverso
"""

import os
import sys
import json
import subprocess
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional
import webbrowser
import socket

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UnityIntegrationManager:
    """
    Gestor de integración con Unity Hub para gráficos avanzados
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.unity_project_path = self.project_path / "unity-metaverse"
        self.backend_url = "http://localhost:3000"
        self.websocket_url = "ws://localhost:3000"
        
        # Configuración de Unity
        self.unity_config = {
            "project_name": "Ciudad Robot Metaverso",
            "unity_version": "2023.3.0f1",  # Versión LTS recomendada
            "render_pipeline": "URP",  # Universal Render Pipeline
            "platform": "PC, Mac & Linux Standalone",
            "graphics_api": ["Direct3D11", "OpenGL", "Vulkan"],
            "target_resolution": "1920x1080",
            "quality_level": "Ultra"
        }
        
        # Configuración de conexión
        self.connection_config = {
            "backend_api": f"{self.backend_url}/api",
            "websocket_endpoint": f"{self.websocket_url}/socket.io",
            "update_frequency": 60,  # FPS
            "sync_interval": 1000  # ms
        }
        
        logger.info("Unity Integration Manager inicializado")
    
    def check_unity_installation(self) -> Dict[str, bool]:
        """Verificar si Unity Hub y Unity Editor están instalados"""
        checks = {
            "unity_hub": False,
            "unity_editor": False,
            "visual_studio": False
        }
        
        # Rutas comunes de Unity Hub
        unity_hub_paths = [
            r"C:\Program Files\Unity Hub\Unity Hub.exe",
            r"C:\Program Files (x86)\Unity Hub\Unity Hub.exe",
            os.path.expanduser("~/Applications/Unity Hub.app/Contents/MacOS/Unity Hub"),
            "/opt/unityhub/unityhub"  # Linux
        ]
        
        for path in unity_hub_paths:
            if os.path.exists(path):
                checks["unity_hub"] = True
                self.unity_hub_path = path
                break
        
        # Verificar Unity Editor
        if checks["unity_hub"]:
            # Buscar instalaciones de Unity
            unity_installs_path = os.path.expanduser("~/AppData/Roaming/UnityHub/installs.json")
            if os.path.exists(unity_installs_path):
                try:
                    with open(unity_installs_path, 'r') as f:
                        installs = json.load(f)
                        if installs:
                            checks["unity_editor"] = True
                except:
                    pass
        
        # Verificar Visual Studio (para scripting C#)
        vs_paths = [
            r"C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.exe",
            r"C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\devenv.exe"
        ]
        
        for path in vs_paths:
            if os.path.exists(path):
                checks["visual_studio"] = True
                break
        
        return checks
    
    def create_unity_project_structure(self):
        """Crear estructura del proyecto Unity"""
        try:
            # Crear directorio del proyecto Unity
            self.unity_project_path.mkdir(exist_ok=True)
            
            # Estructura de carpetas del proyecto Unity
            folders = [
                "Assets",
                "Assets/Scripts",
                "Assets/Scripts/Managers",
                "Assets/Scripts/Controllers",
                "Assets/Scripts/Network",
                "Assets/Scripts/UI",
                "Assets/Prefabs",
                "Assets/Prefabs/Robots",
                "Assets/Prefabs/Buildings",
                "Assets/Prefabs/Equipment",
                "Assets/Materials",
                "Assets/Textures",
                "Assets/Models",
                "Assets/Models/Robots",
                "Assets/Models/Buildings",
                "Assets/Animations",
                "Assets/Audio",
                "Assets/Scenes",
                "Assets/Resources",
                "ProjectSettings",
                "Packages"
            ]
            
            for folder in folders:
                (self.unity_project_path / folder).mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Estructura del proyecto Unity creada en: {self.unity_project_path}")
            
            # Crear archivos de configuración
            self._create_unity_config_files()
            self._create_unity_scripts()
            
        except Exception as e:
            logger.error(f"Error creando estructura del proyecto Unity: {e}")
            raise
    
    def _create_unity_config_files(self):
        """Crear archivos de configuración de Unity"""
        
        # ProjectSettings/ProjectVersion.txt
        project_version = f"""m_EditorVersion: {self.unity_config['unity_version']}
m_EditorVersionWithRevision: {self.unity_config['unity_version']} (1)
"""
        
        with open(self.unity_project_path / "ProjectSettings" / "ProjectVersion.txt", 'w') as f:
            f.write(project_version)
        
        # Packages/manifest.json
        manifest = {
            "dependencies": {
                "com.unity.render-pipelines.universal": "14.0.8",
                "com.unity.textmeshpro": "3.0.6",
                "com.unity.timeline": "1.7.4",
                "com.unity.ugui": "1.0.0",
                "com.unity.visualscripting": "1.8.0",
                "com.unity.modules.ai": "1.0.0",
                "com.unity.modules.animation": "1.0.0",
                "com.unity.modules.audio": "1.0.0",
                "com.unity.modules.physics": "1.0.0",
                "com.unity.modules.physics2d": "1.0.0",
                "com.unity.modules.ui": "1.0.0",
                "com.unity.modules.networking": "1.0.0"
            }
        }
        
        with open(self.unity_project_path / "Packages" / "manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info("Archivos de configuración de Unity creados")
    
    def _create_unity_scripts(self):
        """Crear scripts principales de Unity"""
        
        # GameManager principal
        game_manager_script = '''using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using SocketIOClient;

namespace CiudadRobot
{
    public class GameManager : MonoBehaviour
    {
        [Header("Configuración de Conexión")]
        public string backendUrl = "http://localhost:3000";
        public string websocketUrl = "ws://localhost:3000";
        
        [Header("Managers")]
        public NetworkManager networkManager;
        public CityManager cityManager;
        public RobotManager robotManager;
        public UIManager uiManager;
        
        private SocketIOUnity socket;
        
        void Start()
        {
            InitializeGame();
            ConnectToBackend();
        }
        
        void InitializeGame()
        {
            Debug.Log("Inicializando Ciudad Robot Metaverso...");
            
            // Inicializar managers
            if (networkManager != null) networkManager.Initialize();
            if (cityManager != null) cityManager.Initialize();
            if (robotManager != null) robotManager.Initialize();
            if (uiManager != null) uiManager.Initialize();
        }
        
        void ConnectToBackend()
        {
            try
            {
                // Configurar WebSocket
                socket = new SocketIOUnity(websocketUrl);
                
                socket.OnConnected += (sender, e) =>
                {
                    Debug.Log("Conectado al backend del metaverso");
                    uiManager?.ShowConnectionStatus(true);
                };
                
                socket.OnDisconnected += (sender, e) =>
                {
                    Debug.Log("Desconectado del backend");
                    uiManager?.ShowConnectionStatus(false);
                };
                
                // Eventos del sistema
                socket.On("robot_update", OnRobotUpdate);
                socket.On("city_update", OnCityUpdate);
                socket.On("manufacturing_update", OnManufacturingUpdate);
                socket.On("research_update", OnResearchUpdate);
                
                socket.Connect();
            }
            catch (System.Exception ex)
            {
                Debug.LogError($"Error conectando al backend: {ex.Message}");
            }
        }
        
        void OnRobotUpdate(SocketIOResponse response)
        {
            Debug.Log("Actualización de robot recibida");
            // Procesar actualización de robot
            robotManager?.HandleRobotUpdate(response.GetValue<string>());
        }
        
        void OnCityUpdate(SocketIOResponse response)
        {
            Debug.Log("Actualización de ciudad recibida");
            // Procesar actualización de ciudad
            cityManager?.HandleCityUpdate(response.GetValue<string>());
        }
        
        void OnManufacturingUpdate(SocketIOResponse response)
        {
            Debug.Log("Actualización de manufacturing recibida");
            // Procesar actualización de manufacturing
        }
        
        void OnResearchUpdate(SocketIOResponse response)
        {
            Debug.Log("Actualización de investigación recibida");
            // Procesar actualización de investigación
        }
        
        void OnDestroy()
        {
            if (socket != null)
            {
                socket.Disconnect();
            }
        }
    }
}
'''
        
        # NetworkManager para comunicación con backend
        network_manager_script = '''using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.Text;

namespace CiudadRobot
{
    public class NetworkManager : MonoBehaviour
    {
        [Header("Configuración API")]
        public string apiBaseUrl = "http://localhost:3000/api";
        
        public void Initialize()
        {
            Debug.Log("NetworkManager inicializado");
        }
        
        // Obtener estado de la ciudad
        public IEnumerator GetCityStatus()
        {
            string url = $"{apiBaseUrl}/city/status";
            
            using (UnityWebRequest request = UnityWebRequest.Get(url))
            {
                yield return request.SendWebRequest();
                
                if (request.result == UnityWebRequest.Result.Success)
                {
                    string jsonResponse = request.downloadHandler.text;
                    Debug.Log($"Estado de la ciudad: {jsonResponse}");
                    // Procesar respuesta
                }
                else
                {
                    Debug.LogError($"Error obteniendo estado de ciudad: {request.error}");
                }
            }
        }
        
        // Obtener robots activos
        public IEnumerator GetActiveRobots()
        {
            string url = $"{apiBaseUrl}/robots/active";
            
            using (UnityWebRequest request = UnityWebRequest.Get(url))
            {
                yield return request.SendWebRequest();
                
                if (request.result == UnityWebRequest.Result.Success)
                {
                    string jsonResponse = request.downloadHandler.text;
                    Debug.Log($"Robots activos: {jsonResponse}");
                    // Procesar respuesta
                }
                else
                {
                    Debug.LogError($"Error obteniendo robots: {request.error}");
                }
            }
        }
        
        // Enviar comando a robot
        public IEnumerator SendRobotCommand(string robotId, string command, string parameters)
        {
            string url = $"{apiBaseUrl}/robots/{robotId}/command";
            
            var commandData = new
            {
                command = command,
                parameters = parameters,
                timestamp = System.DateTime.Now.ToString("yyyy-MM-ddTHH:mm:ss.fffZ")
            };
            
            string jsonData = JsonUtility.ToJson(commandData);
            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
            
            using (UnityWebRequest request = new UnityWebRequest(url, "POST"))
            {
                request.uploadHandler = new UploadHandlerRaw(bodyRaw);
                request.downloadHandler = new DownloadHandlerBuffer();
                request.SetRequestHeader("Content-Type", "application/json");
                
                yield return request.SendWebRequest();
                
                if (request.result == UnityWebRequest.Result.Success)
                {
                    Debug.Log($"Comando enviado exitosamente: {request.downloadHandler.text}");
                }
                else
                {
                    Debug.LogError($"Error enviando comando: {request.error}");
                }
            }
        }
    }
}
'''
        
        # CityManager para gestión de la ciudad
        city_manager_script = '''using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace CiudadRobot
{
    public class CityManager : MonoBehaviour
    {
        [Header("Edificios y Estructuras")]
        public GameObject[] buildingPrefabs;
        public GameObject[] factoryPrefabs;
        public GameObject[] labPrefabs;
        
        [Header("Configuración de Ciudad")]
        public Vector3 cityCenter = Vector3.zero;
        public float cityRadius = 1000f;
        public int maxBuildings = 100;
        
        private Dictionary<string, GameObject> instantiatedBuildings;
        
        public void Initialize()
        {
            Debug.Log("CityManager inicializado");
            instantiatedBuildings = new Dictionary<string, GameObject>();
            GenerateInitialCity();
        }
        
        void GenerateInitialCity()
        {
            // Generar ciudad inicial
            CreateCentralHub();
            CreateManufacturingDistrict();
            CreateResearchDistrict();
            CreateSecurityPerimeter();
        }
        
        void CreateCentralHub()
        {
            // Crear hub central de IA
            Vector3 hubPosition = cityCenter;
            GameObject hub = CreateBuilding("central_hub", hubPosition, "AI_Hub");
            
            if (hub != null)
            {
                // Añadir efectos especiales al hub central
                AddSpecialEffects(hub, "ai_core");
            }
        }
        
        void CreateManufacturingDistrict()
        {
            // Crear distrito de manufacturing
            for (int i = 0; i < 5; i++)
            {
                Vector3 position = cityCenter + new Vector3(
                    Random.Range(-200f, 200f),
                    0f,
                    Random.Range(-200f, 200f)
                );
                
                CreateBuilding($"factory_{i}", position, "Robot_Factory");
            }
        }
        
        void CreateResearchDistrict()
        {
            // Crear distrito de investigación
            for (int i = 0; i < 3; i++)
            {
                Vector3 position = cityCenter + new Vector3(
                    Random.Range(-300f, 300f),
                    0f,
                    Random.Range(-300f, 300f)
                );
                
                CreateBuilding($"lab_{i}", position, "Research_Lab");
            }
        }
        
        void CreateSecurityPerimeter()
        {
            // Crear perímetro de seguridad
            int numTowers = 8;
            for (int i = 0; i < numTowers; i++)
            {
                float angle = (360f / numTowers) * i * Mathf.Deg2Rad;
                Vector3 position = cityCenter + new Vector3(
                    Mathf.Cos(angle) * cityRadius * 0.8f,
                    0f,
                    Mathf.Sin(angle) * cityRadius * 0.8f
                );
                
                CreateBuilding($"security_tower_{i}", position, "Security_Tower");
            }
        }
        
        GameObject CreateBuilding(string buildingId, Vector3 position, string buildingType)
        {
            GameObject prefab = GetBuildingPrefab(buildingType);
            if (prefab == null)
            {
                Debug.LogWarning($"Prefab no encontrado para tipo: {buildingType}");
                return null;
            }
            
            GameObject building = Instantiate(prefab, position, Quaternion.identity);
            building.name = $"{buildingType}_{buildingId}";
            
            instantiatedBuildings[buildingId] = building;
            
            Debug.Log($"Edificio creado: {buildingId} en posición {position}");
            return building;
        }
        
        GameObject GetBuildingPrefab(string buildingType)
        {
            // Retornar prefab apropiado basado en el tipo
            // Por ahora retornamos un cubo básico
            GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
            cube.transform.localScale = new Vector3(10f, 5f, 10f);
            
            // Asignar color basado en tipo
            Renderer renderer = cube.GetComponent<Renderer>();
            switch (buildingType)
            {
                case "AI_Hub":
                    renderer.material.color = Color.cyan;
                    break;
                case "Robot_Factory":
                    renderer.material.color = Color.yellow;
                    break;
                case "Research_Lab":
                    renderer.material.color = Color.green;
                    break;
                case "Security_Tower":
                    renderer.material.color = Color.red;
                    break;
                default:
                    renderer.material.color = Color.gray;
                    break;
            }
            
            return cube;
        }
        
        void AddSpecialEffects(GameObject building, string effectType)
        {
            // Añadir efectos especiales como partículas, luces, etc.
            Light buildingLight = building.AddComponent<Light>();
            buildingLight.color = Color.cyan;
            buildingLight.intensity = 2f;
            buildingLight.range = 50f;
        }
        
        public void HandleCityUpdate(string updateData)
        {
            Debug.Log($"Procesando actualización de ciudad: {updateData}");
            // Procesar actualizaciones en tiempo real
        }
    }
}
'''
        
        # Escribir scripts
        scripts_path = self.unity_project_path / "Assets" / "Scripts"
        
        with open(scripts_path / "GameManager.cs", 'w', encoding='utf-8') as f:
            f.write(game_manager_script)
        
        with open(scripts_path / "Managers" / "NetworkManager.cs", 'w', encoding='utf-8') as f:
            f.write(network_manager_script)
        
        with open(scripts_path / "Managers" / "CityManager.cs", 'w', encoding='utf-8') as f:
            f.write(city_manager_script)
        
        logger.info("Scripts principales de Unity creados")
    
    def create_launch_script(self):
        """Crear script de lanzamiento integrado"""
        
        launch_script = f'''#!/usr/bin/env python
"""
Launcher Integrado para Ciudad Robot Metaverso
Lanza backend Python + Unity Hub + Frontend
"""

import asyncio
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

class MetaverseLauncher:
    def __init__(self):
        self.project_path = Path(__file__).parent
        self.backend_process = None
        self.unity_process = None
        
    async def launch_backend(self):
        """Lanzar servidor backend"""
        print("🚀 Iniciando servidor backend...")
        
        backend_path = self.project_path / "backend"
        if backend_path.exists():
            try:
                self.backend_process = subprocess.Popen([
                    sys.executable, "server.js"
                ], cwd=backend_path)
                print("✅ Backend iniciado en http://localhost:3000")
                await asyncio.sleep(2)  # Esperar a que inicie
            except Exception as e:
                print(f"❌ Error iniciando backend: {{e}}")
        
    async def launch_unity(self):
        """Lanzar Unity Hub y proyecto"""
        print("🎮 Iniciando Unity Hub...")
        
        unity_project = self.project_path / "unity-metaverse"
        
        # Comandos para diferentes sistemas operativos
        unity_commands = [
            r"C:\\Program Files\\Unity Hub\\Unity Hub.exe",  # Windows
            "/Applications/Unity Hub.app/Contents/MacOS/Unity Hub",  # macOS
            "unityhub"  # Linux
        ]
        
        for cmd in unity_commands:
            try:
                if Path(cmd).exists() or cmd == "unityhub":
                    self.unity_process = subprocess.Popen([
                        cmd, "--projectPath", str(unity_project)
                    ])
                    print("✅ Unity Hub iniciado")
                    break
            except Exception:
                continue
        else:
            print("⚠️  Unity Hub no encontrado. Instálalo desde: https://unity.com/download")
    
    async def launch_web_interface(self):
        """Abrir interfaz web"""
        print("🌐 Abriendo interfaz web...")
        await asyncio.sleep(3)  # Esperar a que el backend esté listo
        
        try:
            webbrowser.open("http://localhost:3000")
            print("✅ Interfaz web abierta")
        except Exception as e:
            print(f"❌ Error abriendo navegador: {{e}}")
    
    async def launch_all(self):
        """Lanzar todo el sistema"""
        print("🌟 INICIANDO CIUDAD ROBOT METAVERSO 🌟")
        print("=" * 50)
        
        # Lanzar en paralelo
        await asyncio.gather(
            self.launch_backend(),
            self.launch_unity(),
            self.launch_web_interface()
        )
        
        print("\\n🎉 METAVERSO LISTO!")
        print("📱 Interfaz Web: http://localhost:3000")
        print("🎮 Unity: Abrir en Unity Hub")
        print("🔧 Backend API: http://localhost:3000/api")
        print("\\nPresiona Ctrl+C para detener...")
        
        # Mantener activo
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\\n🛑 Deteniendo metaverso...")
            self.cleanup()
    
    def cleanup(self):
        """Limpiar procesos"""
        if self.backend_process:
            self.backend_process.terminate()
        if self.unity_process:
            self.unity_process.terminate()
        print("🧹 Procesos terminados")

if __name__ == "__main__":
    launcher = MetaverseLauncher()
    asyncio.run(launcher.launch_all())
'''
        
        with open(self.project_path / "launch_metaverse.py", 'w', encoding='utf-8') as f:
            f.write(launch_script)
        
        # Hacer ejecutable en Unix
        if sys.platform != 'win32':
            os.chmod(self.project_path / "launch_metaverse.py", 0o755)
        
        logger.info("Script de lanzamiento creado: launch_metaverse.py")
    
    def create_unity_installation_guide(self):
        """Crear guía de instalación de Unity"""
        
        guide = """# 🎮 Guía de Instalación - Unity Hub para Ciudad Robot Metaverso

## 📋 Requisitos del Sistema

### Mínimos:
- **OS**: Windows 10 64-bit / macOS 10.14+ / Ubuntu 18.04+
- **CPU**: Intel Core i5-4590 / AMD FX 8350 equivalente
- **RAM**: 8 GB
- **GPU**: NVIDIA GTX 970 / AMD R9 280 equivalente
- **DirectX**: Version 11
- **Almacenamiento**: 20 GB espacio libre

### Recomendados para Gráficos Avanzados:
- **CPU**: Intel Core i7-8700K / AMD Ryzen 7 2700X
- **RAM**: 16 GB+
- **GPU**: NVIDIA RTX 3070 / AMD RX 6700 XT
- **Almacenamiento**: SSD con 50 GB espacio libre

## 🚀 Instalación Paso a Paso

### 1. Descargar Unity Hub
1. Ve a: https://unity.com/download
2. Descarga **Unity Hub** (gratuito)
3. Ejecuta el instalador y sigue las instrucciones

### 2. Instalar Unity Editor
1. Abre Unity Hub
2. Ve a la pestaña **"Installs"**
3. Clic en **"Install Editor"**
4. Selecciona **Unity 2023.3 LTS** (recomendado)
5. En **"Add modules"** incluye:
   - ✅ **Microsoft Visual Studio Community** (Windows)
   - ✅ **Windows Build Support** (IL2CPP)
   - ✅ **Universal Windows Platform Build Support**
   - ✅ **WebGL Build Support**
   - ✅ **Android Build Support** (opcional)

### 3. Configurar Licencia
1. En Unity Hub, ve a **"Settings" → "License Management"**
2. Clic en **"Activate New License"**
3. Selecciona **"Unity Personal"** (gratuito para uso personal)
4. Inicia sesión con tu Unity ID

### 4. Abrir Proyecto del Metaverso
1. En Unity Hub, clic en **"Add"**
2. Navega a: `C:\\Users\\Brian Carlisle\\mundo virtual\\unity-metaverse`
3. Selecciona la carpeta y clic **"Add Project"**
4. Doble clic en el proyecto para abrirlo

## 🎨 Configuración de Gráficos Avanzados

### Universal Render Pipeline (URP):
- **Rendering Path**: Forward
- **Depth Texture**: Enabled
- **Opaque Texture**: Enabled
- **HDR**: Enabled
- **MSAA**: 4x (ajustar según rendimiento)

### Post-Processing:
- **Bloom**: Enabled
- **Color Grading**: LDR
- **Vignette**: Subtle
- **Screen Space Ambient Occlusion**: Enabled

### Lighting:
- **Lighting Mode**: Mixed
- **Realtime Global Illumination**: Enabled
- **Baked Global Illumination**: Enabled
- **Auto Generate**: Enabled

## 🔧 Configuración de Red

### Para Conectar con Backend:
1. En Unity, ve a **Edit → Project Settings → Player**
2. En **"Configuration"**:
   - **Scripting Backend**: IL2CPP
   - **Api Compatibility Level**: .NET Standard 2.1

### Paquetes Necesarios:
- **Universal RP**: 14.0.8
- **TextMeshPro**: 3.0.6
- **ProBuilder**: 5.0.6 (para construcción de niveles)
- **Cinemachine**: 2.9.7 (para cámaras cinematográficas)

## 🌐 Conexión con Backend

### Configurar NetworkManager:
```csharp
public string backendUrl = "http://localhost:3000";
public string websocketUrl = "ws://localhost:3000";
```

### Test de Conexión:
1. Ejecuta el backend Python: `python launch_metaverse.py`
2. En Unity, presiona **Play**
3. Verifica en **Console** los mensajes de conexión

## 🎯 Escenas Principales

### MainScene:
- **GameManager**: Control principal del juego
- **NetworkManager**: Conexión con backend
- **CityManager**: Gestión de la ciudad
- **RobotManager**: Control de robots
- **UIManager**: Interfaz de usuario

### Navegación:
- **WASD**: Mover cámara
- **Mouse**: Rotar vista
- **Scroll**: Zoom
- **F**: Enfocar objeto seleccionado

## 🚀 Lanzamiento Rápido

### Opción 1 - Script Automático:
```bash
python launch_metaverse.py
```

### Opción 2 - Manual:
1. Ejecutar backend: `python backend/server.py`
2. Abrir Unity Hub
3. Seleccionar proyecto "Ciudad Robot Metaverso"
4. Presionar **Play** en Unity Editor

## 🔍 Solución de Problemas

### Error de Conexión:
- Verificar que el backend esté ejecutándose en puerto 3000
- Comprobar firewall/antivirus
- Verificar URL en NetworkManager

### Rendimiento Bajo:
- Reducir configuración de gráficos
- Desactivar post-processing
- Reducir MSAA a 2x o desactivar

### Scripts No Compilan:
- Verificar .NET Framework instalado
- Reimportar scripts: **Assets → Reimport All**
- Verificar paquetes instalados

## 📞 Soporte

- **Unity Documentation**: https://docs.unity3d.com/
- **Unity Learn**: https://learn.unity.com/
- **Unity Community**: https://unity.com/community

¡Disfruta explorando tu Ciudad Robot Metaverso! 🤖🌆
"""
        
        with open(self.project_path / "UNITY_INSTALLATION.md", 'w', encoding='utf-8') as f:
            f.write(guide)
        
        logger.info("Guía de instalación de Unity creada: UNITY_INSTALLATION.md")
    
    def generate_installation_summary(self) -> Dict[str, str]:
        """Generar resumen de instalación"""
        
        checks = self.check_unity_installation()
        
        return {
            "unity_hub_status": "✅ Instalado" if checks["unity_hub"] else "❌ No instalado - Descargar de unity.com",
            "unity_editor_status": "✅ Instalado" if checks["unity_editor"] else "❌ No instalado - Instalar desde Unity Hub",
            "visual_studio_status": "✅ Instalado" if checks["visual_studio"] else "⚠️ Recomendado - Para scripting C#",
            "project_path": str(self.unity_project_path),
            "next_steps": [
                "1. Instalar Unity Hub si no está instalado",
                "2. Instalar Unity Editor 2023.3 LTS desde Unity Hub",
                "3. Ejecutar: python launch_metaverse.py",
                "4. Abrir proyecto en Unity Hub",
                "5. Presionar Play para entrar al metaverso"
            ]
        }

# Función principal
def setup_unity_integration(project_path: str = None):
    """
    Configurar integración completa con Unity Hub
    """
    if project_path is None:
        project_path = os.getcwd()
    
    manager = UnityIntegrationManager(project_path)
    
    # Verificar instalación
    checks = manager.check_unity_installation()
    
    print("🎮 CONFIGURACIÓN UNITY HUB - CIUDAD ROBOT METAVERSO")
    print("=" * 60)
    
    for component, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {component.replace('_', ' ').title()}: {'Instalado' if status else 'No instalado'}")
    
    # Crear estructura del proyecto
    print("\n📁 Creando estructura del proyecto Unity...")
    manager.create_unity_project_structure()
    
    # Crear scripts de lanzamiento
    print("🚀 Creando launcher integrado...")
    manager.create_launch_script()
    
    # Crear guía de instalación
    print("📚 Creando guía de instalación...")
    manager.create_unity_installation_guide()
    
    # Resumen final
    summary = manager.generate_installation_summary()
    
    print("\n🎯 RESUMEN DE CONFIGURACIÓN:")
    print("-" * 40)
    for key, value in summary.items():
        if key != "next_steps":
            print(f"• {key.replace('_', ' ').title()}: {value}")
    
    print("\n📋 PRÓXIMOS PASOS:")
    for step in summary["next_steps"]:
        print(f"  {step}")
    
    print(f"\n🎉 ¡Configuración completada!")
    print(f"📂 Proyecto Unity: {manager.unity_project_path}")
    print(f"🚀 Launcher: python launch_metaverse.py")
    print(f"📖 Guía completa: UNITY_INSTALLATION.md")
    
    return manager

if __name__ == "__main__":
    setup_unity_integration()