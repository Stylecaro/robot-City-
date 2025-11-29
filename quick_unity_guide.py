"""
RESUMEN RÁPIDO - Unity Hub Metaverso
Pasos esenciales para ver el proyecto en Unity Hub
"""

def quick_unity_steps():
    print("""
    🎮 PASOS RÁPIDOS PARA VER EN UNITY HUB:
    
    ══════════════════════════════════════════════════════════════
    
    1️⃣ ABRIR UNITY HUB
       • Ya está ejecutándose (6 procesos activos)
       • Si no aparece, hacer clic en icono de Unity Hub
    
    2️⃣ CREAR/ABRIR PROYECTO
       NUEVO:
       • Projects → New project → 3D Core
       • Nombre: "CiudadRobotMetaverso"
       • Location: C:\\Users\\Brian Carlisle\\mundo virtual
       
       EXISTENTE:
       • Projects → Open
       • Seleccionar: C:\\Users\\Brian Carlisle\\mundo virtual\\UnityProject
    
    3️⃣ CONFIGURAR ESCENA
       • Crear GameObject vacío llamado "GameManager"
       • Añadir script GameManager.cs (ya existe en carpeta)
       • Presionar ▶️ PLAY
    
    4️⃣ VER LA CIUDAD 3D
       • 4 edificios de colores (Manufacturing, Research, Security, AI)
       • Terreno verde de 20x20
       • Navegar con Alt + ratón
    
    ══════════════════════════════════════════════════════════════
    
    🎯 RESULTADO: Ciudad Robot 3D funcionando en Unity!
    
    """)

if __name__ == "__main__":
    quick_unity_steps()
    
    # Verificar estado de Unity Hub
    import subprocess
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Unity Hub.exe'], 
                              capture_output=True, text=True, shell=True)
        if 'Unity Hub.exe' in result.stdout:
            print("✅ Unity Hub confirmado ejecutándose")
            lines = [line for line in result.stdout.split('\n') if 'Unity Hub.exe' in line]
            print(f"📊 Procesos Unity Hub activos: {len(lines)}")
        else:
            print("❌ Unity Hub no detectado")
    except:
        print("⚠️ No se pudo verificar Unity Hub")
        
    print("\n🚀 Usa 'unity_hub_menu.bat' para opciones interactivas")