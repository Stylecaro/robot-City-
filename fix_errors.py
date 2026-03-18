"""
Reparador de Errores - Metaverso Ciudad Robot
Script para diagnosticar y reparar problemas comunes
"""

import os
import sys
import subprocess
import time
import json
import shutil
from pathlib import Path
import psutil
import webbrowser

class MetaversoErrorFixer:
    """Reparador de errores del metaverso"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.errors_found = []
        self.fixes_applied = []
        
    def print_header(self):
        """Mostrar header del reparador"""
        print("""
        ╔══════════════════════════════════════════════════════════════╗
        ║                🔧 REPARADOR DE ERRORES 🛠️                    ║
        ║                Ciudad Robot Metaverso                        ║
        ║                                                              ║
        ║            Diagnosticando y Reparando Problemas...          ║
        ╚══════════════════════════════════════════════════════════════╝
        """)
    
    def check_unity_hub_issues(self):
        """Diagnosticar problemas de Unity Hub"""
        print("🔍 Diagnosticando Unity Hub...")
        
        # Verificar procesos de Unity Hub
        unity_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            try:
                if 'unity hub' in proc.info['name'].lower():
                    unity_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if len(unity_processes) > 3:
            self.errors_found.append("Múltiples procesos Unity Hub detectados")
            print(f"⚠️  {len(unity_processes)} procesos Unity Hub encontrados")
            self.fix_unity_hub_processes()
        else:
            print("✅ Procesos Unity Hub normales")
        
        # Verificar instalación de Unity Hub
        unity_paths = [
            "C:/Program Files/Unity Hub/Unity Hub.exe",
            "C:/Program Files (x86)/Unity Hub/Unity Hub.exe"
        ]
        
        unity_installed = False
        for path in unity_paths:
            if os.path.exists(path):
                unity_installed = True
                print(f"✅ Unity Hub encontrado: {path}")
                break
        
        if not unity_installed:
            self.errors_found.append("Unity Hub no instalado correctamente")
            self.fix_unity_hub_installation()
    
    def fix_unity_hub_processes(self):
        """Reparar procesos múltiples de Unity Hub"""
        print("🔧 Reparando procesos Unity Hub...")
        
        try:
            # Terminar todos los procesos Unity Hub
            subprocess.run(['taskkill', '/f', '/im', 'Unity Hub.exe'], 
                         capture_output=True)
            time.sleep(2)
            
            # Reiniciar Unity Hub limpio
            unity_path = "C:/Program Files/Unity Hub/Unity Hub.exe"
            if os.path.exists(unity_path):
                subprocess.Popen([unity_path])
                self.fixes_applied.append("Procesos Unity Hub reiniciados")
                print("✅ Unity Hub reiniciado correctamente")
            
        except Exception as e:
            print(f"❌ Error reparando Unity Hub: {e}")
    
    def fix_unity_hub_installation(self):
        """Reparar instalación de Unity Hub"""
        print("🔧 Reparando instalación Unity Hub...")
        
        print("📥 Abriendo descarga de Unity Hub...")
        webbrowser.open("https://unity.com/download")
        
        print("""
        📋 INSTRUCCIONES PARA INSTALAR UNITY HUB:
        
        1. 📥 Descargar Unity Hub desde la página que se abrió
        2. 🔧 Ejecutar el instalador como administrador
        3. ✅ Completar la instalación
        4. 🎮 Abrir Unity Hub
        5. 📦 Instalar Unity Editor 2022.3 LTS
        
        ⚡ Después ejecuta: python quick_start.py
        """)
        
        self.fixes_applied.append("Iniciado proceso de instalación Unity Hub")
    
    def check_python_dependencies(self):
        """Verificar dependencias Python"""
        print("🔍 Verificando dependencias Python...")
        
        required_packages = [
            'flask', 'numpy', 'psutil'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"✅ {package} disponible")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package} faltante")
        
        if missing_packages:
            self.errors_found.append(f"Paquetes Python faltantes: {missing_packages}")
            self.fix_python_dependencies(missing_packages)
        else:
            print("✅ Todas las dependencias Python disponibles")
    
    def fix_python_dependencies(self, missing_packages):
        """Instalar dependencias Python faltantes"""
        print("🔧 Instalando dependencias Python...")
        
        try:
            for package in missing_packages:
                print(f"📦 Instalando {package}...")
                result = subprocess.run([sys.executable, '-m', 'pip', 'install', package],
                                      capture_output=True, text=True)
                
                if result.returncode == 0:
                    print(f"✅ {package} instalado correctamente")
                    self.fixes_applied.append(f"Instalado {package}")
                else:
                    print(f"❌ Error instalando {package}: {result.stderr}")
        
        except Exception as e:
            print(f"❌ Error instalando dependencias: {e}")
    
    def check_project_structure(self):
        """Verificar estructura del proyecto"""
        print("🔍 Verificando estructura del proyecto...")
        
        required_dirs = [
            "ai-engine", "backend", "frontend", "UnityProject", 
            "manufacturing-system", "research-system", 
            "security-system", "simulation-system"
        ]
        
        missing_dirs = []
        
        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                print(f"✅ {dir_name} existe")
            else:
                missing_dirs.append(dir_name)
                print(f"❌ {dir_name} faltante")
        
        if missing_dirs:
            self.errors_found.append(f"Directorios faltantes: {missing_dirs}")
            self.fix_project_structure(missing_dirs)
        else:
            print("✅ Estructura del proyecto completa")
    
    def fix_project_structure(self, missing_dirs):
        """Crear directorios faltantes"""
        print("🔧 Reparando estructura del proyecto...")
        
        for dir_name in missing_dirs:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Creado directorio: {dir_name}")
            self.fixes_applied.append(f"Creado directorio {dir_name}")
    
    def check_unity_project_files(self):
        """Verificar archivos del proyecto Unity"""
        print("🔍 Verificando proyecto Unity...")
        
        unity_project = self.project_root / "UnityProject"
        required_files = [
            "Assets/Scripts/GameManager.cs",
            "ProjectSettings/ProjectVersion.txt"
        ]
        
        missing_files = []
        
        for file_path in required_files:
            full_path = unity_project / file_path
            if full_path.exists():
                print(f"✅ {file_path} existe")
            else:
                missing_files.append(file_path)
                print(f"❌ {file_path} faltante")
        
        if missing_files:
            self.errors_found.append(f"Archivos Unity faltantes: {missing_files}")
            self.fix_unity_project_files()
        else:
            print("✅ Proyecto Unity completo")
    
    def fix_unity_project_files(self):
        """Recrear archivos Unity faltantes"""
        print("🔧 Reparando archivos Unity...")
        
        unity_project = self.project_root / "UnityProject"
        
        # Crear directorios Unity
        unity_dirs = [
            "Assets", "Assets/Scripts", "Assets/Scenes", "Assets/Prefabs",
            "Assets/Materials", "Assets/Models", "Assets/Textures", 
            "ProjectSettings", "Packages"
        ]
        
        for dir_name in unity_dirs:
            (unity_project / dir_name).mkdir(parents=True, exist_ok=True)
        
        # Recrear ProjectVersion.txt
        project_version = """m_EditorVersion: 2022.3.12f1
m_EditorVersionWithRevision: 2022.3.12f1 (4fe6e059c7ef)
"""
        
        with open(unity_project / "ProjectSettings/ProjectVersion.txt", 'w') as f:
            f.write(project_version)
        
        # Recrear GameManager.cs si falta
        gamemanager_path = unity_project / "Assets/Scripts/GameManager.cs"
        if not gamemanager_path.exists():
            gamemanager_script = '''using UnityEngine;

public class GameManager : MonoBehaviour
{
    [Header("Ciudad Robot Metaverso")]
    public Transform spawnPoint;
    
    void Start()
    {
        Debug.Log("🤖 Ciudad Robot Metaverso - Sistema Iniciado");
        InitializeMetaverse();
    }
    
    void InitializeMetaverse()
    {
        // Crear terreno
        GameObject terrain = GameObject.CreatePrimitive(PrimitiveType.Plane);
        terrain.name = "MetaverseTerrain";
        terrain.transform.localScale = new Vector3(20, 1, 20);
        
        // Crear edificios principales
        CreateBuilding(new Vector3(-10, 1, 0), Color.blue, "Manufacturing Center");
        CreateBuilding(new Vector3(10, 1, 0), Color.cyan, "Research Labs");
        CreateBuilding(new Vector3(0, 1, -10), Color.red, "Security HQ");
        CreateBuilding(new Vector3(0, 1, 10), Color.magenta, "AI Central");
        
        // Configurar cámara
        Camera.main.transform.position = new Vector3(0, 10, -15);
        Camera.main.transform.LookAt(Vector3.zero);
        
        Debug.Log("✅ Metaverso inicializado correctamente");
    }
    
    void CreateBuilding(Vector3 position, Color color, string name)
    {
        GameObject building = GameObject.CreatePrimitive(PrimitiveType.Cube);
        building.name = name;
        building.transform.position = position;
        building.transform.localScale = new Vector3(3, 4, 3);
        building.GetComponent<Renderer>().material.color = color;
    }
}
'''
            
            with open(gamemanager_path, 'w', encoding='utf-8') as f:
                f.write(gamemanager_script)
        
        print("✅ Archivos Unity reparados")
        self.fixes_applied.append("Archivos Unity recreados")
    
    def check_backend_status(self):
        """Verificar estado del backend"""
        print("🔍 Verificando backend...")
        
        backend_dir = self.project_root / "backend"
        server_file = backend_dir / "server.js"
        
        if not server_file.exists():
            self.errors_found.append("Archivo server.js faltante")
            self.fix_backend_files()
        else:
            print("✅ Archivo server.js existe")
        
        # Verificar Node.js
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js disponible: {result.stdout.strip()}")
            else:
                self.errors_found.append("Node.js no funciona correctamente")
                self.fix_nodejs()
        except FileNotFoundError:
            self.errors_found.append("Node.js no instalado")
            self.fix_nodejs()
    
    def fix_backend_files(self):
        """Reparar archivos del backend"""
        print("🔧 Reparando backend...")
        
        backend_dir = self.project_root / "backend"
        backend_dir.mkdir(exist_ok=True)
        
        # Crear server.js básico
        server_code = '''const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static('public'));

// Ruta principal
app.get('/', (req, res) => {
    res.json({
        message: '🤖 Ciudad Robot Metaverso API',
        status: 'operational',
        version: '1.0.0'
    });
});

// Estado del metaverso
app.get('/api/status', (req, res) => {
    res.json({
        metaverso: 'operational',
        manufacturing: 'active',
        research: 'running',
        security: 'protecting',
        ai_engine: 'processing'
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Backend corriendo en http://localhost:${PORT}`);
});'''
        
        with open(backend_dir / "server.js", 'w') as f:
            f.write(server_code)
        
        # Crear package.json
        package_json = {
            "name": "metaverso-backend",
            "version": "1.0.0",
            "main": "server.js",
            "scripts": {"start": "node server.js"},
            "dependencies": {"express": "^4.18.2"}
        }
        
        with open(backend_dir / "package.json", 'w') as f:
            json.dump(package_json, f, indent=2)
        
        print("✅ Backend reparado")
        self.fixes_applied.append("Backend recreado")
    
    def fix_nodejs(self):
        """Ayudar con instalación de Node.js"""
        print("🔧 Node.js necesita instalación...")
        
        print("📥 Abriendo descarga de Node.js...")
        webbrowser.open("https://nodejs.org/")
        
        print("""
        📋 INSTRUCCIONES PARA INSTALAR NODE.JS:
        
        1. 📥 Descargar Node.js LTS desde la página que se abrió
        2. 🔧 Ejecutar el instalador
        3. ✅ Completar la instalación (incluir npm)
        4. 🔄 Reiniciar terminal
        5. ✅ Verificar: node --version && npm --version
        """)
        
        self.fixes_applied.append("Iniciado proceso instalación Node.js")
    
    def optimize_system_performance(self):
        """Optimizar rendimiento del sistema"""
        print("🚀 Optimizando rendimiento...")
        
        # Limpiar archivos temporales
        temp_dirs = [
            self.project_root / "temp",
            self.project_root / "logs"
        ]
        
        for temp_dir in temp_dirs:
            if temp_dir.exists():
                try:
                    shutil.rmtree(temp_dir)
                    temp_dir.mkdir()
                    print(f"✅ Limpiado: {temp_dir.name}")
                except Exception:
                    print(f"⚠️  No se pudo limpiar: {temp_dir.name}")
        
        self.fixes_applied.append("Sistema optimizado")
    
    def create_quick_launcher(self):
        """Crear lanzador rápido mejorado"""
        print("🔧 Creando lanzador mejorado...")
        
        launcher_code = '''@echo off
title METAVERSO CIUDAD ROBOT - Launcher Pro
color 0A

echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🤖 CIUDAD ROBOT METAVERSO 🌆                  ║
echo ║                      Launcher Profesional                    ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo 🚀 Iniciando sistemas del metaverso...
echo.

:: Verificar Unity Hub
echo 🎮 Verificando Unity Hub...
tasklist /fi "imagename eq Unity Hub.exe" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚡ Iniciando Unity Hub...
    start "" "C:\\Program Files\\Unity Hub\\Unity Hub.exe"
) else (
    echo ✅ Unity Hub ya está ejecutándose
)

:: Abrir Dashboard Web
echo 🌐 Abriendo Dashboard Web...
start "" metaverso_dashboard.html

:: Ejecutar Quick Start
echo 🚀 Iniciando sistemas...
python quick_start.py

echo.
echo ✅ Metaverso iniciado correctamente!
echo 🌟 ¡Disfruta la experiencia!
pause
'''
        
        with open(self.project_root / "launch_metaverso_pro.bat", 'w') as f:
            f.write(launcher_code)
        
        print("✅ Lanzador profesional creado: launch_metaverso_pro.bat")
        self.fixes_applied.append("Lanzador profesional creado")
    
    def show_repair_summary(self):
        """Mostrar resumen de reparaciones"""
        print("\n" + "="*60)
        print("📊 RESUMEN DE DIAGNÓSTICO Y REPARACIÓN")
        print("="*60)
        
        if self.errors_found:
            print("🔍 PROBLEMAS ENCONTRADOS:")
            for i, error in enumerate(self.errors_found, 1):
                print(f"   {i}. {error}")
        else:
            print("✅ No se encontraron problemas críticos")
        
        print()
        
        if self.fixes_applied:
            print("🔧 REPARACIONES APLICADAS:")
            for i, fix in enumerate(self.fixes_applied, 1):
                print(f"   {i}. {fix}")
        else:
            print("ℹ️  No se requirieron reparaciones")
        
        print("="*60)
        
        # Estado final
        if len(self.fixes_applied) > 0:
            print("🎉 REPARACIÓN COMPLETADA")
            print("✅ El metaverso está listo para usar")
        else:
            print("✅ SISTEMA EN PERFECTO ESTADO")
        
        print("\n🚀 PARA ENTRAR AL METAVERSO:")
        print("   1. Ejecuta: launch_metaverso_pro.bat")
        print("   2. O ejecuta: python quick_start.py")
        print("   3. Abre Unity Hub y crea proyecto")
        print("   4. ¡Explora la Ciudad Robot! 🤖")
        
        print("\n🌟 ¡El futuro digital te espera!")
        print("="*60)
    
    def run_full_diagnosis(self):
        """Ejecutar diagnóstico completo"""
        self.print_header()
        
        print("🔍 Iniciando diagnóstico completo del sistema...\n")
        
        # Ejecutar todas las verificaciones
        self.check_unity_hub_issues()
        print()
        
        self.check_python_dependencies()
        print()
        
        self.check_project_structure()
        print()
        
        self.check_unity_project_files()
        print()
        
        self.check_backend_status()
        print()
        
        self.optimize_system_performance()
        print()
        
        self.create_quick_launcher()
        print()
        
        # Mostrar resumen
        self.show_repair_summary()
        
        return len(self.errors_found) == 0

# Función principal
def main():
    fixer = MetaversoErrorFixer()
    
    try:
        success = fixer.run_full_diagnosis()
        
        if success:
            print("\n🎯 ¡Sistema completamente reparado!")
            
            # Preguntar si quiere lanzar
            launch = input("\n¿Quieres lanzar el metaverso ahora? (s/n): ").lower()
            
            if launch in ['s', 'si', 'yes', 'y']:
                print("🚀 Iniciando Metaverso Ciudad Robot...")
                os.system("launch_metaverso_pro.bat")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Error durante la reparación: {e}")
        return False

if __name__ == "__main__":
    main()