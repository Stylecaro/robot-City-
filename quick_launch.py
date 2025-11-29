"""
Lanzador Rápido del Metaverso - Ciudad Robot
Configuración automática y entrada al mundo virtual 3D
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_unity_hub():
    """Verificar si Unity Hub está instalado"""
    unity_paths = [
        r"C:\Program Files\Unity Hub\Unity Hub.exe",
        r"C:\Program Files (x86)\Unity Hub\Unity Hub.exe"
    ]
    
    for path in unity_paths:
        if os.path.exists(path):
            return path
    return None

def open_unity_hub():
    """Abrir Unity Hub"""
    unity_path = check_unity_hub()
    
    if unity_path:
        print("🎮 Abriendo Unity Hub...")
        try:
            subprocess.Popen([unity_path], shell=True)
            print("✅ Unity Hub abierto")
            return True
        except Exception as e:
            print(f"❌ Error abriendo Unity Hub: {e}")
    else:
        print("❌ Unity Hub no encontrado")
        print("📥 Descárgalo desde: https://unity.com/download")
        webbrowser.open("https://unity.com/download")
    
    return False

def launch_backend():
    """Lanzar backend si existe"""
    backend_path = Path("backend")
    
    if backend_path.exists():
        try:
            print("🚀 Iniciando backend...")
            subprocess.Popen([sys.executable, "-m", "http.server", "3000"], 
                           cwd=backend_path, shell=True)
            print("✅ Backend mock iniciado en puerto 3000")
            return True
        except Exception as e:
            print(f"⚠️ Error iniciando backend: {e}")
    
    return False

def open_web_interface():
    """Abrir interfaz web"""
    print("🌐 Abriendo interfaz web...")
    try:
        webbrowser.open("http://localhost:3000")
        print("✅ Navegador abierto")
    except Exception as e:
        print(f"❌ Error abriendo navegador: {e}")

def main():
    """Función principal de lanzamiento"""
    print("🌟" + "="*50 + "🌟")
    print("   🤖 CIUDAD ROBOT METAVERSO - LANZADOR 🏙️")
    print("🌟" + "="*50 + "🌟")
    print()
    
    # Mostrar información del proyecto
    project_path = Path.cwd()
    unity_project = project_path / "unity-metaverse"
    
    print(f"📂 Proyecto: {project_path}")
    print(f"🎮 Unity Project: {unity_project}")
    print()
    
    # Verificar Unity Hub
    print("🔍 Verificando Unity Hub...")
    unity_available = open_unity_hub()
    
    if unity_available:
        print()
        print("📋 INSTRUCCIONES UNITY:")
        print("1. En Unity Hub, clic en 'Installs'")
        print("2. Instalar Unity 2023.3 LTS")
        print("3. En 'Projects', clic 'Add' y seleccionar:")
        print(f"   {unity_project}")
        print("4. Abrir proyecto y presionar ▶️ Play")
        print()
    
    # Lanzar backend (simulado)
    print("🔧 Configurando backend...")
    launch_backend()
    
    # Esperar un poco
    time.sleep(2)
    
    # Abrir web
    open_web_interface()
    
    print()
    print("🎉 METAVERSO CONFIGURADO!")
    print("📱 Web: http://localhost:3000")
    print("🎮 Unity: Instalar Editor desde Unity Hub")
    print("📖 Guía: UNITY_INSTALLATION.md")
    print()
    print("⚡ Para entrar al metaverso:")
    print("   1. Instalar Unity Editor 2023.3 LTS")
    print("   2. Abrir proyecto en Unity Hub")
    print("   3. Presionar Play en Unity")
    print()
    print("Presiona Enter para continuar...")
    input()

if __name__ == "__main__":
    main()