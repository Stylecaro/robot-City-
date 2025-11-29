# 🎮 Guía de Instalación - Unity Hub para Ciudad Robot Metaverso

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
2. Navega a: `C:\Users\Brian Carlisle\mundo virtual\unity-metaverse`
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
