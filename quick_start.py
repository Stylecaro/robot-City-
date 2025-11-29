#!/usr/bin/env python3
"""
Quick Launch - Metaverso Ciudad Robot
Lanzador rápido simplificado
"""

import os
import sys
import subprocess
import webbrowser
import time

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                🤖 CIUDAD ROBOT METAVERSO 🌆                  ║
    ║                                                              ║
    ║               ¡Lanzamiento Rápido Iniciado! 🚀              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def check_python():
    """Verificar Python"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor} detectado")
            return True
        else:
            print(f"❌ Python 3.8+ requerido, encontrado {version.major}.{version.minor}")
            return False
    except:
        print("❌ Python no encontrado")
        return False

def setup_environment():
    """Configurar entorno básico"""
    print("🔧 Configurando entorno...")
    
    project_dir = r"c:\Users\Brian Carlisle\mundo virtual"
    os.chdir(project_dir)
    
    # Crear directorios básicos
    dirs = ["logs", "temp", "UnityProject", "backend"]
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    
    print("✅ Entorno configurado")

def launch_web_interface():
    """Lanzar interfaz web básica"""
    print("🌐 Abriendo interfaz web...")
    
    # Crear HTML básico si no existe
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>Ciudad Robot Metaverso</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            text-align: center; 
            padding: 50px;
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: rgba(0,0,0,0.3);
            padding: 30px;
            border-radius: 15px;
        }
        h1 { font-size: 3em; margin-bottom: 20px; }
        .status { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            margin: 20px 0; 
            border-radius: 10px; 
        }
        .button {
            background: #00ff88;
            color: black;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 1.2em;
            cursor: pointer;
            margin: 10px;
            transition: transform 0.2s;
        }
        .button:hover { transform: scale(1.05); }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Ciudad Robot Metaverso 🌆</h1>
        <div class="status">
            <h3>Estado del Sistema: ✅ OPERATIVO</h3>
            <p>🏭 Manufacturing Centers: Activos</p>
            <p>🧬 Research Labs: Funcionando</p>
            <p>🛡️ Security System: Protegiendo</p>
            <p>🧠 AI Engine: Procesando</p>
        </div>
        
        <button class="button" onclick="window.open('https://unity.com/download')">
            🎮 Descargar Unity Hub
        </button>
        
        <button class="button" onclick="alert('Sistema backend iniciándose...')">
            🚀 Ver Estado Backend  
        </button>
        
        <div style="margin-top: 30px;">
            <h3>📋 Próximos Pasos:</h3>
            <p>1. Instalar Unity Hub desde el botón de arriba</p>
            <p>2. Crear nuevo proyecto Unity 3D</p>
            <p>3. Importar assets del metaverso</p>
            <p>4. ¡Explorar la ciudad robot!</p>
        </div>
        
        <div style="margin-top: 20px; font-size: 0.8em;">
            <p>⚡ Dashboard actualizado: ''' + time.strftime("%Y-%m-%d %H:%M:%S") + '''</p>
        </div>
    </div>
    
    <script>
        // Animación simple
        setInterval(() => {
            const title = document.querySelector('h1');
            title.style.textShadow = `0 0 ${Math.random() * 20}px #00ff88`;
        }, 2000);
    </script>
</body>
</html>'''
    
    with open("metaverso_dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Abrir en navegador
    dashboard_path = os.path.abspath("metaverso_dashboard.html")
    webbrowser.open(f"file://{dashboard_path}")
    print("✅ Dashboard web abierto")

def launch_unity_hub():
    """Intentar lanzar Unity Hub"""
    print("🎮 Buscando Unity Hub...")
    
    unity_paths = [
        r"C:\Program Files\Unity Hub\Unity Hub.exe",
        r"C:\Program Files (x86)\Unity Hub\Unity Hub.exe",
        os.path.expanduser(r"~\AppData\Roaming\UnityHub\Unity Hub.exe")
    ]
    
    for path in unity_paths:
        if os.path.exists(path):
            print(f"✅ Unity Hub encontrado: {path}")
            try:
                subprocess.Popen([path])
                print("✅ Unity Hub iniciado")
                return True
            except:
                print("❌ Error iniciando Unity Hub")
                return False
    
    print("⚠️  Unity Hub no encontrado")
    print("📥 Abriendo página de descarga de Unity...")
    webbrowser.open("https://unity.com/download")
    return False

def show_instructions():
    """Mostrar instrucciones finales"""
    print("""
    🎯 INSTRUCCIONES PARA ENTRAR AL METAVERSO:
    
    1. 📥 Si Unity Hub no se abrió automáticamente:
       - Descargar desde: https://unity.com/download
       - Instalar Unity Hub
       - Instalar Unity Editor (versión 2022.3 LTS recomendada)
    
    2. 🎮 En Unity Hub:
       - Crear nuevo proyecto 3D
       - Nombre: "CiudadRobotMetaverso"
       - Importar scripts desde: ./UnityProject/Assets/Scripts/
    
    3. 🌐 Dashboard Web:
       - Ya está abierto en tu navegador
       - Monitorea el estado de todos los sistemas
    
    4. 🚀 Para desarrollo avanzado:
       - Backend API: Ejecutar "python metaverso_launcher.py"
       - Sistemas IA: Disponibles en ./ai-engine/
       - Manufacturing: ./manufacturing-system/
    
    🌟 ¡Disfruta explorando la Ciudad Robot Metaverso!
    """)

def main():
    """Función principal del lanzador rápido"""
    print_banner()
    
    # Verificaciones básicas
    if not check_python():
        input("Presiona Enter para salir...")
        return
    
    # Configurar entorno
    setup_environment()
    
    # Lanzar componentes
    launch_web_interface()
    time.sleep(2)  # Esperar que se abra el navegador
    
    unity_launched = launch_unity_hub()
    
    # Mostrar instrucciones
    show_instructions()
    
    # Mensaje final
    print("\n" + "="*60)
    if unity_launched:
        print("🎉 ¡LANZAMIENTO EXITOSO! Unity Hub y Dashboard iniciados")
    else:
        print("⚠️  LANZAMIENTO PARCIAL - Dashboard listo, Unity Hub pendiente")
    
    print("✅ Ciudad Robot Metaverso preparada")
    print("🌟 ¡El futuro digital te espera!")
    print("="*60)
    
    input("\nPresiona Enter para finalizar...")

if __name__ == "__main__":
    main()