#!/usr/bin/env python
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
                print(f"❌ Error iniciando backend: {e}")
        
    async def launch_unity(self):
        """Lanzar Unity Hub y proyecto"""
        print("🎮 Iniciando Unity Hub...")
        
        unity_project = self.project_path / "unity-metaverse"
        
        # Comandos para diferentes sistemas operativos
        unity_commands = [
            r"C:\Program Files\Unity Hub\Unity Hub.exe",  # Windows
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
            print(f"❌ Error abriendo navegador: {e}")
    
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
        
        print("\n🎉 METAVERSO LISTO!")
        print("📱 Interfaz Web: http://localhost:3000")
        print("🎮 Unity: Abrir en Unity Hub")
        print("🔧 Backend API: http://localhost:3000/api")
        print("\nPresiona Ctrl+C para detener...")
        
        # Mantener activo
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo metaverso...")
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
