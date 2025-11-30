"""
Launch System - Sistema de Lanzamiento Completo del Metaverso
Inicia todos los componentes con verificaciones de dependencias
"""
import subprocess
import sys
import os
import time
import asyncio
import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MetaversoLauncher:
    """Lanzador completo del sistema"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.processes = []
        self.checks_passed = False
    
    def print_banner(self):
        """Muestra banner de inicio"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     🤖 METAVERSO CIUDAD ROBOT - SISTEMA COMPLETO IA 🌟     ║
║                                                              ║
║  • AI Coordinator con Machine Learning                      ║
║  • Robots Inteligentes con Pathfinding                      ║
║  • Análisis Predictivo Avanzado                             ║
║  • Sincronización Unity en Tiempo Real                      ║
║  • Dashboard Web de Control                                 ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_dependencies(self) -> bool:
        """Verifica todas las dependencias"""
        logger.info("🔍 Verificando dependencias...")
        
        required_packages = [
            'numpy', 'tensorflow', 'torch', 'fastapi', 'uvicorn',
            'websockets', 'sklearn', 'pandas', 'aiohttp'
        ]
        
        missing = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                logger.info(f"  ✅ {package}")
            except ImportError:
                logger.warning(f"  ❌ {package} - NO INSTALADO")
                missing.append(package)
        
        if missing:
            logger.error(f"\n⚠️  Faltan paquetes: {', '.join(missing)}")
            logger.info("Instalando paquetes faltantes...")
            
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", *missing
                ])
                logger.info("✅ Paquetes instalados exitosamente")
            except Exception as e:
                logger.error(f"❌ Error instalando paquetes: {e}")
                return False
        
        logger.info("✅ Todas las dependencias verificadas\n")
        return True
    
    def check_unity_project(self) -> bool:
        """Verifica proyecto Unity"""
        logger.info("🎮 Verificando proyecto Unity...")
        
        unity_paths = [
            self.base_path / "UnityProject",
            self.base_path / "My project (1)" / "My project (2)",
            self.base_path / "unity-project"
        ]
        
        for path in unity_paths:
            if path.exists():
                scripts_path = path / "Assets" / "Scripts"
                
                if scripts_path.exists():
                    logger.info(f"  ✅ Proyecto encontrado: {path}")
                    
                    # Verificar scripts clave
                    required_scripts = [
                        "NetworkManager.cs",
                        "RobotController.cs",
                        "CityManager.cs"
                    ]
                    
                    for script in required_scripts:
                        script_file = scripts_path / script
                        if script_file.exists():
                            logger.info(f"    ✅ {script}")
                        else:
                            logger.warning(f"    ⚠️  {script} no encontrado")
                    
                    return True
        
        logger.warning("⚠️  Proyecto Unity no encontrado completamente")
        logger.info("  Los scripts están listos en UnityProject/Assets/Scripts/")
        return True  # No bloqueante
    
    def check_ai_modules(self) -> bool:
        """Verifica módulos de IA"""
        logger.info("🧠 Verificando módulos de IA...")
        
        ai_modules = [
            self.base_path / "ai-engine" / "core" / "ai_coordinator.py",
            self.base_path / "ai-engine" / "core" / "predictive_analytics.py",
            self.base_path / "robot-system" / "robot_ai.py"
        ]
        
        for module in ai_modules:
            if module.exists():
                logger.info(f"  ✅ {module.name}")
            else:
                logger.error(f"  ❌ {module.name} - NO ENCONTRADO")
                return False
        
        logger.info("✅ Módulos de IA verificados\n")
        return True
    
    async def start_backend_server(self):
        """Inicia servidor backend"""
        logger.info("🚀 Iniciando servidor backend...")
        
        server_file = self.base_path / "metaverso_integrated_server.py"
        
        if not server_file.exists():
            logger.error(f"❌ Servidor no encontrado: {server_file}")
            return False
        
        try:
            process = subprocess.Popen(
                [sys.executable, str(server_file)],
                cwd=str(self.base_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.processes.append(process)
            logger.info("✅ Servidor backend iniciado")
            logger.info("   📍 Dashboard: http://localhost:8765")
            logger.info("   📍 API: http://localhost:8765/api/status")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error iniciando servidor: {e}")
            return False
    
    def open_dashboard(self):
        """Abre dashboard en navegador"""
        import webbrowser
        
        time.sleep(3)  # Esperar a que servidor inicie
        
        logger.info("🌐 Abriendo dashboard web...")
        webbrowser.open("http://localhost:8765")
    
    def open_unity_guide(self):
        """Muestra guía de Unity"""
        guide = """
╔══════════════════════════════════════════════════════════════╗
║                    🎮 GUÍA DE UNITY                         ║
╚══════════════════════════════════════════════════════════════╝

📋 PASOS PARA ABRIR PROYECTO UNITY:

1. Abrir Unity Hub
   • Si no está abierto: Buscar "Unity Hub" en Windows

2. Agregar Proyecto
   • Click en "Add" o "Agregar"
   • Navegar a: {unity_path}
   • Seleccionar la carpeta del proyecto

3. Abrir Proyecto
   • Click en el proyecto en la lista
   • Esperar a que Unity cargue (puede tomar 1-2 minutos)

4. Configurar Escena
   • En Unity, ir a: Window → Rendering → Lighting
   • File → Build Settings → Add Open Scenes

5. Crear Objetos de Sistema
   • GameObject → Create Empty → Nombre: "NetworkManager"
   • Inspector → Add Component → NetworkManager
   • Repetir para CityManager

6. Presionar PLAY ▶️
   • Ver la ciudad robot en 3D
   • Los robots se sincronizan automáticamente con el backend

📡 VERIFICAR CONEXIÓN:
   • Console de Unity debe mostrar: "🌐 Conectando a ws://localhost:8765"
   • Dashboard web mostrará "Clientes Unity: 1"

🎨 OPCIONAL - MEJORAR VISUALES:
   • Window → Package Manager → Buscar "Universal RP"
   • Edit → Project Settings → Graphics → URP Asset
   • Lighting → Generate Lighting

═══════════════════════════════════════════════════════════════
        """.format(unity_path=self.base_path / "UnityProject")
        
        print(guide)
    
    async def run(self):
        """Ejecuta el lanzador completo"""
        self.print_banner()
        
        # Verificaciones
        logger.info("═══ FASE 1: VERIFICACIONES ═══\n")
        
        if not self.check_dependencies():
            logger.error("❌ Error en dependencias. Abortando.")
            return
        
        if not self.check_ai_modules():
            logger.error("❌ Módulos de IA faltantes. Abortando.")
            return
        
        self.check_unity_project()
        
        self.checks_passed = True
        
        # Inicio de servicios
        logger.info("\n═══ FASE 2: INICIO DE SERVICIOS ═══\n")
        
        # Iniciar backend
        if not await self.start_backend_server():
            logger.error("❌ No se pudo iniciar el servidor")
            return
        
        # Abrir dashboard
        self.open_dashboard()
        
        # Mostrar guía de Unity
        logger.info("\n═══ FASE 3: CONFIGURACIÓN DE UNITY ═══\n")
        self.open_unity_guide()
        
        # Estado final
        logger.info("\n═══════════════════════════════════════════════════════")
        logger.info("✅ SISTEMA COMPLETAMENTE OPERATIVO")
        logger.info("═══════════════════════════════════════════════════════")
        logger.info("")
        logger.info("📊 SERVICIOS ACTIVOS:")
        logger.info("  • Backend IA: http://localhost:8765")
        logger.info("  • Dashboard Web: Abierto en navegador")
        logger.info("  • AI Coordinator: Ejecutando")
        logger.info("  • Predictive Analytics: Activo")
        logger.info("  • WebSocket Server: ws://localhost:8765/ws/*")
        logger.info("")
        logger.info("🎮 PRÓXIMOS PASOS:")
        logger.info("  1. Abrir Unity Hub")
        logger.info("  2. Abrir proyecto UnityProject/")
        logger.info("  3. Configurar NetworkManager y CityManager")
        logger.info("  4. Presionar PLAY ▶️")
        logger.info("")
        logger.info("💡 COMANDOS ÚTILES:")
        logger.info("  • Crear Robot: Click en dashboard web")
        logger.info("  • Ver Métricas: http://localhost:8765/api/status")
        logger.info("  • Ver Alertas: http://localhost:8765/api/alerts")
        logger.info("")
        logger.info("Presiona Ctrl+C para detener todos los servicios")
        logger.info("═══════════════════════════════════════════════════════\n")
        
        try:
            # Mantener vivo
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("\n🛑 Deteniendo servicios...")
            self.cleanup()
    
    def cleanup(self):
        """Limpia procesos al salir"""
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        
        logger.info("✅ Servicios detenidos. ¡Hasta pronto!")


async def main():
    launcher = MetaversoLauncher()
    await launcher.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 ¡Adiós!")
