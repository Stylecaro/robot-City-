"""
Reparador Simple - Metaverso Ciudad Robot
Versión simplificada sin dependencias externas
"""

import os
import sys
import subprocess
import time
import json
import webbrowser
from pathlib import Path

class SimpleMetaversoFixer:
    """Reparador simple del metaverso"""
    
    def __init__(self):
        self.project_root = Path("c:/Users/Brian Carlisle/mundo virtual")
        self.errors_found = []
        self.fixes_applied = []
        
    def print_header(self):
        """Mostrar header del reparador"""
        print("""
        ╔══════════════════════════════════════════════════════════════╗
        ║                🔧 REPARADOR SIMPLE 🛠️                        ║
        ║                Ciudad Robot Metaverso                        ║
        ║                                                              ║
        ║            Diagnosticando y Reparando Problemas...          ║
        ╚══════════════════════════════════════════════════════════════╝
        """)
    
    def check_unity_hub(self):
        """Verificar Unity Hub de forma simple"""
        print("🔍 Verificando Unity Hub...")
        
        # Verificar instalación
        unity_paths = [
            "C:/Program Files/Unity Hub/Unity Hub.exe",
            "C:/Program Files (x86)/Unity Hub/Unity Hub.exe"
        ]
        
        unity_found = False
        for path in unity_paths:
            if os.path.exists(path):
                unity_found = True
                print(f"✅ Unity Hub encontrado: {path}")
                self.unity_path = path
                break
        
        if not unity_found:
            self.errors_found.append("Unity Hub no encontrado")
            self.fix_unity_hub()
            return False
        
        # Intentar abrir Unity Hub
        try:
            print("🎮 Abriendo Unity Hub...")
            subprocess.Popen([self.unity_path])
            self.fixes_applied.append("Unity Hub iniciado")
            print("✅ Unity Hub abierto correctamente")
            return True
        except Exception as e:
            print(f"❌ Error abriendo Unity Hub: {e}")
            return False
    
    def fix_unity_hub(self):
        """Reparar Unity Hub"""
        print("🔧 Unity Hub necesita instalación...")
        
        print("📥 Abriendo descarga de Unity Hub...")
        webbrowser.open("https://unity.com/download")
        
        print("""
        📋 PASOS PARA INSTALAR UNITY HUB:
        
        1. 📥 Descargar Unity Hub desde la página web
        2. 🔧 Ejecutar instalador como administrador  
        3. ✅ Completar instalación
        4. 🎮 Abrir Unity Hub
        5. 📦 Instalar Unity Editor 2022.3 LTS
        6. 🚀 Ejecutar nuevamente este script
        """)
        
        self.fixes_applied.append("Iniciado proceso instalación Unity Hub")
    
    def check_project_files(self):
        """Verificar archivos del proyecto"""
        print("🔍 Verificando archivos del proyecto...")
        
        # Verificar directorios principales
        required_dirs = [
            "ai-engine", "backend", "frontend", "UnityProject", 
            "manufacturing-system", "research-system"
        ]
        
        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                print(f"✅ {dir_name}")
            else:
                missing_dirs.append(dir_name)
                print(f"❌ {dir_name} faltante")
        
        if missing_dirs:
            self.fix_project_structure(missing_dirs)
        
        # Verificar archivos clave
        key_files = [
            "quick_start.py",
            "metaverso_launcher.py", 
            "metaverso_dashboard.html"
        ]
        
        for file_name in key_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                print(f"✅ {file_name}")
            else:
                print(f"❌ {file_name} faltante")
                self.errors_found.append(f"Archivo {file_name} faltante")
    
    def fix_project_structure(self, missing_dirs):
        """Crear directorios faltantes"""
        print("🔧 Creando directorios faltantes...")
        
        for dir_name in missing_dirs:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Creado: {dir_name}")
            self.fixes_applied.append(f"Creado directorio {dir_name}")
    
    def create_unity_project(self):
        """Crear proyecto Unity básico"""
        print("🎮 Configurando proyecto Unity...")
        
        unity_dir = self.project_root / "UnityProject"
        unity_dir.mkdir(exist_ok=True)
        
        # Crear subdirectorios
        subdirs = [
            "Assets", "Assets/Scripts", "Assets/Scenes", 
            "ProjectSettings", "Packages"
        ]
        
        for subdir in subdirs:
            (unity_dir / subdir).mkdir(parents=True, exist_ok=True)
        
        # ProjectVersion.txt
        project_version = """m_EditorVersion: 2022.3.12f1
m_EditorVersionWithRevision: 2022.3.12f1 (4fe6e059c7ef)"""
        
        with open(unity_dir / "ProjectSettings/ProjectVersion.txt", 'w') as f:
            f.write(project_version)
        
        # GameManager.cs básico
        gamemanager = '''using UnityEngine;

public class GameManager : MonoBehaviour
{
    void Start()
    {
        Debug.Log("🤖 ¡Bienvenido a Ciudad Robot Metaverso!");
        CreateBasicWorld();
    }
    
    void CreateBasicWorld()
    {
        // Crear terreno
        GameObject ground = GameObject.CreatePrimitive(PrimitiveType.Plane);
        ground.name = "Ground";
        ground.transform.localScale = new Vector3(10, 1, 10);
        
        // Edificios de la ciudad
        CreateBuilding(new Vector3(-5, 1, 0), Color.blue, "Manufacturing");
        CreateBuilding(new Vector3(5, 1, 0), Color.green, "Research Lab");
        CreateBuilding(new Vector3(0, 1, -5), Color.red, "Security HQ");
        CreateBuilding(new Vector3(0, 1, 5), Color.yellow, "AI Center");
        
        // Configurar cámara
        Camera.main.transform.position = new Vector3(0, 8, -12);
        Camera.main.transform.LookAt(Vector3.zero);
        
        Debug.Log("✅ Mundo básico creado - ¡Explora la ciudad!");
    }
    
    GameObject CreateBuilding(Vector3 pos, Color color, string name)
    {
        GameObject building = GameObject.CreatePrimitive(PrimitiveType.Cube);
        building.name = name;
        building.transform.position = pos;
        building.transform.localScale = new Vector3(2, 3, 2);
        building.GetComponent<Renderer>().material.color = color;
        return building;
    }
}'''
        
        with open(unity_dir / "Assets/Scripts/GameManager.cs", 'w', encoding='utf-8') as f:
            f.write(gamemanager)
        
        print("✅ Proyecto Unity configurado")
        self.fixes_applied.append("Proyecto Unity creado")
    
    def create_launch_scripts(self):
        """Crear scripts de lanzamiento"""
        print("🚀 Creando scripts de lanzamiento...")
        
        # Script batch mejorado
        batch_script = '''@echo off
title CIUDAD ROBOT METAVERSO
color 0A
cls

echo.
echo    ╔════════════════════════════════════════╗
echo    ║        🤖 CIUDAD ROBOT METAVERSO 🌆    ║  
echo    ║              Launcher v2.0             ║
echo    ╚════════════════════════════════════════╝
echo.

cd /d "c:\\Users\\Brian Carlisle\\mundo virtual"

echo 🔍 Verificando sistema...

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado
    pause
    exit /b
)
echo ✅ Python disponible

:: Iniciar Unity Hub si no está ejecutándose
echo 🎮 Iniciando Unity Hub...
tasklist /fi "imagename eq Unity Hub.exe" /fo csv 2>NUL | find /I "Unity Hub.exe" >NUL
if %errorlevel% neq 0 (
    if exist "C:\\Program Files\\Unity Hub\\Unity Hub.exe" (
        start "" "C:\\Program Files\\Unity Hub\\Unity Hub.exe"
        echo ✅ Unity Hub iniciado
    ) else (
        echo ⚠️  Unity Hub no encontrado - instalar desde unity.com
    )
) else (
    echo ✅ Unity Hub ya ejecutándose
)

:: Abrir dashboard web
echo 🌐 Abriendo dashboard...
if exist metaverso_dashboard.html (
    start "" metaverso_dashboard.html
    echo ✅ Dashboard abierto
) else (
    echo ⚠️  Dashboard no encontrado
)

:: Ejecutar sistema principal
echo 🚀 Iniciando metaverso...
python quick_start.py

echo.
echo 🌟 ¡Sistema iniciado! Revisa Unity Hub y el navegador
echo.
pause
'''
        
        with open(self.project_root / "start_metaverso.bat", 'w') as f:
            f.write(batch_script)
        
        print("✅ Script de lanzamiento creado")
        self.fixes_applied.append("Scripts de lanzamiento creados")
    
    def test_system_launch(self):
        """Probar lanzamiento del sistema"""
        print("🧪 Probando lanzamiento del sistema...")
        
        # Verificar que los archivos principales existen
        key_files = [
            "quick_start.py",
            "metaverso_dashboard.html",
            "start_metaverso.bat"
        ]
        
        all_ready = True
        for file_name in key_files:
            if (self.project_root / file_name).exists():
                print(f"✅ {file_name} listo")
            else:
                print(f"❌ {file_name} faltante")
                all_ready = False
        
        if all_ready:
            print("🎉 ¡Sistema listo para lanzar!")
            return True
        else:
            print("⚠️  Sistema parcialmente listo")
            return False
    
    def show_final_instructions(self):
        """Mostrar instrucciones finales"""
        print("\n" + "="*60)
        print("🎯 INSTRUCCIONES FINALES")
        print("="*60)
        
        if self.errors_found:
            print("⚠️  PROBLEMAS ENCONTRADOS:")
            for error in self.errors_found:
                print(f"   • {error}")
            print()
        
        if self.fixes_applied:
            print("✅ REPARACIONES APLICADAS:")
            for fix in self.fixes_applied:
                print(f"   • {fix}")
            print()
        
        print("🚀 PARA ENTRAR AL METAVERSO:")
        print("   1. 🎮 Unity Hub debería estar abierto")
        print("   2. 📁 En Unity Hub: Open > Seleccionar carpeta UnityProject")
        print("   3. 🌐 Dashboard web debería estar en el navegador")
        print("   4. 🔄 Si hay problemas, ejecuta: start_metaverso.bat")
        print()
        print("📋 EN UNITY:")
        print("   1. 📦 Crear nuevo proyecto 3D si es necesario")
        print("   2. 📂 Importar GameManager.cs desde Assets/Scripts")
        print("   3. 🎬 Crear escena nueva y añadir GameManager")
        print("   4. ▶️  Presionar Play para ver la ciudad")
        print()
        print("🌟 ¡Disfruta explorando Ciudad Robot Metaverso!")
        print("="*60)
    
    def run_repair(self):
        """Ejecutar reparación completa"""
        self.print_header()
        
        print("🔍 Iniciando diagnóstico y reparación...\n")
        
        # Verificaciones y reparaciones
        unity_ok = self.check_unity_hub()
        print()
        
        self.check_project_files()
        print()
        
        self.create_unity_project()
        print()
        
        self.create_launch_scripts()
        print()
        
        system_ready = self.test_system_launch()
        print()
        
        # Mostrar instrucciones finales
        self.show_final_instructions()
        
        return system_ready and unity_ok

def main():
    """Función principal"""
    fixer = SimpleMetaversoFixer()
    
    try:
        success = fixer.run_repair()
        
        if success:
            print("\n🎉 ¡REPARACIÓN EXITOSA!")
            
            # Ofrecer lanzar el sistema
            response = input("\n¿Quieres abrir Unity Hub ahora? (s/n): ").lower()
            if response in ['s', 'si', 'yes', 'y']:
                if hasattr(fixer, 'unity_path'):
                    subprocess.Popen([fixer.unity_path])
                    print("🎮 Unity Hub abierto")
                
            # Abrir dashboard
            dashboard_path = fixer.project_root / "metaverso_dashboard.html"
            if dashboard_path.exists():
                webbrowser.open(f"file://{dashboard_path}")
                print("🌐 Dashboard abierto en navegador")
        
        else:
            print("\n⚠️  Reparación parcial completada")
            print("Revisa las instrucciones de arriba para completar la configuración")
        
    except Exception as e:
        print(f"\n❌ Error durante la reparación: {e}")
        print("Intenta ejecutar el script nuevamente")

if __name__ == "__main__":
    main()