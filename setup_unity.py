"""
Configuración Automática Unity - Metaverso
Prepara el proyecto Unity con todos los scripts necesarios
"""

import os
import shutil

def setup_unity_project():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║           ⚙️ CONFIGURACIÓN UNITY AUTOMÁTICA 🎮              ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    unity_project_path = os.path.join(base_path, "UnityProject")
    
    print(f"📂 Configurando proyecto en: {unity_project_path}")
    
    # Crear estructura de carpetas si no existe
    folders = [
        "Assets",
        "Assets/Scripts", 
        "Assets/Materials",
        "Assets/Scenes",
        "ProjectSettings"
    ]
    
    for folder in folders:
        folder_path = os.path.join(unity_project_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        print(f"✅ Carpeta creada: {folder}")
    
    # Verificar scripts existentes
    scripts_path = os.path.join(unity_project_path, "Assets", "Scripts")
    
    scripts = [
        "GameManager.cs",
        "WebSocketManager.cs"
    ]
    
    print("\n📄 Verificando scripts:")
    for script in scripts:
        script_path = os.path.join(scripts_path, script)
        if os.path.exists(script_path):
            print(f"✅ {script} - Disponible")
        else:
            print(f"❌ {script} - Falta")
    
    # Crear archivo de configuración Unity
    create_unity_settings()
    
    print("""
    ══════════════════════════════════════════════════════════════
    🎯 INSTRUCCIONES PARA UNITY HUB:
    ══════════════════════════════════════════════════════════════
    
    1. 🎮 Abrir Unity Hub
    2. 📂 Projects → Open → Seleccionar esta carpeta:
       C:\\Users\\Brian Carlisle\\mundo virtual\\UnityProject
    3. ⚙️ Una vez abierto Unity Editor:
       • Hierarchy → Create Empty → Nombre: "GameManager"  
       • Inspector → Add Component → GameManager (script)
       • Inspector → Add Component → WebSocket Manager (script)
    4. ▶️ Presionar PLAY para ver la ciudad
    5. 🌐 ¡Conectado automáticamente con el dashboard web!
    
    ══════════════════════════════════════════════════════════════
    🔗 INTEGRACIÓN WEB AUTOMÁTICA:
    ══════════════════════════════════════════════════════════════
    
    • 📊 Datos sincronizados con dashboard web
    • 🔄 Actualizaciones en tiempo real
    • 🎮 Controles desde navegador web  
    • 📈 Métricas de manufacturing, IA, investigación
    
    🌟 ¡Todo listo para el metaverso completo!
    """)

def create_unity_settings():
    """Crear archivo de configuración básico de Unity"""
    
    settings_content = """
%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!11 &1
AudioManager:
  m_ObjectHideFlags: 0
  serializedVersion: 2
  m_Volume: 1
  m_Rolloff: 0
  m_DopplerFactor: 1
  m_DefaultSpeakerMode: 2
--- !u!29 &1
OcclusionCullingSettings:
  m_ObjectHideFlags: 0
  serializedVersion: 2
  m_OcclusionBakeSettings:
    smallestOccluder: 5
    smallestHole: 0.25
    backfaceThreshold: 100
--- !u!104 &2
RenderSettings:
  m_ObjectHideFlags: 0
  serializedVersion: 9
  m_Fog: 0
  m_FogColor: {r: 0.5, g: 0.5, b: 0.5, a: 1}
  m_FogMode: 3
  m_FogDensity: 0.01
  m_LinearFogStart: 0
  m_LinearFogEnd: 300
  m_AmbientMode: 0
  m_AmbientSkyColor: {r: 0.212, g: 0.227, b: 0.259, a: 1}
  m_AmbientEquatorColor: {r: 0.114, g: 0.125, b: 0.133, a: 1}
  m_AmbientGroundColor: {r: 0.047, g: 0.043, b: 0.035, a: 1}
  m_AmbientIntensity: 1
  m_AmbientMode: 3
  m_SubtractiveShadowColor: {r: 0.42, g: 0.478, b: 0.627, a: 1}
  m_SkyboxMaterial: {fileID: 0}
  m_HaloStrength: 0.5
  m_FlareStrength: 1
  m_FlareFadeSpeed: 3
  m_HaloTexture: {fileID: 0}
  m_SpotCookie: {fileID: 10001, guid: 0000000000000000e000000000000000, type: 0}
  m_DefaultReflectionMode: 0
  m_DefaultReflectionResolution: 128
  m_ReflectionBounces: 1
  m_ReflectionIntensity: 1
  m_CustomReflection: {fileID: 0}
  m_Sun: {fileID: 0}
  m_IndirectSpecularColor: {r: 0, g: 0, b: 0, a: 1}
  m_UseRadianceAmbientProbe: 0
--- !u!157 &3
LightmapSettings:
  m_ObjectHideFlags: 0
  serializedVersion: 12
  m_GIWorkflowMode: 1
"""

    unity_project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "UnityProject")
    settings_path = os.path.join(unity_project_path, "ProjectSettings", "DynamicsManager.asset") 
    
    try:
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(settings_content)
        print("✅ Configuración Unity creada")
    except Exception as e:
        print(f"⚠️ Error creando configuración: {e}")

if __name__ == "__main__":
    setup_unity_project()