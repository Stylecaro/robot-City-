# 🎮 CREAR PROYECTO UNITY - PASO A PASO

## PASO 1: Descargar e Instalar Unity Hub

### Descargar Unity Hub:
```
1. Ir a: https://unity.com/download
2. Click en "Download Unity Hub"
3. Ejecutar el instalador descargado
4. Seguir pasos de instalación
```

### Ejecutar desde PowerShell:
```powershell
# Si ya tienes Unity Hub instalado, verificar:
cd "C:\Program Files\Unity Hub"
.\Unity Hub.exe

# O buscar en Start Menu: "Unity Hub"
```

---

## PASO 2: Instalar Unity Editor

### En Unity Hub:

1. **Abrir Unity Hub**
2. Click en **"Installs"** (izquierda)
3. Click en **"Install Editor"**
4. Seleccionar versión: **Unity 2021.3 LTS** (recomendado)
5. Click **"Next"**

### Módulos a instalar (IMPORTANTE):
```
☑ Microsoft Visual Studio Community 2022
☑ Android Build Support
  ☑ Android SDK & NDK Tools
  ☑ OpenJDK
☑ WebGL Build Support
☑ Windows Build Support (IL2CPP)
☑ Documentation
```

6. Click **"Continue"** → **"Install"**
7. **Esperar 20-40 minutos** (descarga ~8GB)

---

## PASO 3: Crear Nuevo Proyecto

### En Unity Hub:

1. Click en pestaña **"Projects"**
2. Click en **"New project"** (arriba derecha)
3. Seleccionar versión: **2021.3.x LTS**

### Configuración del proyecto:

**Template:** 
- Seleccionar: **3D (URP)** - Universal Render Pipeline
  - (Mejor rendimiento para VR y WebGL)

**Project Settings:**
```
Project name: MundoVirtualBattleArena
Location: C:\Users\Brian Carlisle\mundo virtual\unity-project
```

4. Click **"Create project"**
5. **Esperar 5-10 minutos** mientras Unity crea estructura

---

## PASO 4: Configuración Inicial del Proyecto

### Una vez abierto Unity:

#### A. Configurar Quality Settings

```
Edit > Project Settings > Quality

- Seleccionar "Medium" como default
- VSync Count: Every V Blank
- Shadow Resolution: Medium Res
```

#### B. Configurar Player Settings

```
Edit > Project Settings > Player

Company Name: MundoVirtual
Product Name: Battle Arena

Default Icon: (opcional, añadir después)
```

#### C. Configurar Input System (nuevo)

```
Window > Package Manager
Packages: Unity Registry
Buscar: "Input System"
Click "Install"

Cuando pregunte "Enable new Input System?" → YES
Unity se reiniciará
```

---

## PASO 5: Instalar Packages Esenciales

### Window > Package Manager

**Packages ya instalados (verificar):**
- ✅ Universal RP
- ✅ Visual Scripting
- ✅ Cinemachine

**Instalar adicionales:**

1. **ProBuilder** (modelado 3D in-engine)
   - Buscar: "ProBuilder"
   - Click "Install"

2. **Terrain Tools**
   - Buscar: "Terrain Tools"
   - Click "Install"

3. **TextMeshPro**
   - Ya viene instalado
   - Import "TMP Essential Resources" cuando pida

---

## PASO 6: Configurar Estructura de Carpetas

### En Project Window (abajo):

```
Assets/
├── Scenes/
│   ├── MainMenu.unity
│   ├── BattleArena.unity
│   ├── OpenWorld.unity
│   └── RobotShop.unity
├── Scripts/
│   ├── BattleArena/
│   ├── Player/
│   ├── UI/
│   └── Networking/
├── Prefabs/
│   ├── Characters/
│   ├── Vehicles/
│   ├── Weapons/
│   └── Environment/
├── Materials/
├── Textures/
├── Models/
├── Audio/
└── Resources/
    └── Contracts/
```

### Crear carpetas automáticamente:

**Copiar este script y ejecutar en Unity:**

```csharp
// Crear archivo: Assets/Editor/ProjectSetup.cs
using UnityEngine;
using UnityEditor;
using System.IO;

public class ProjectSetup : MonoBehaviour
{
    [MenuItem("Tools/Setup Project Folders")]
    static void SetupFolders()
    {
        string[] folders = new string[]
        {
            "Assets/Scenes",
            "Assets/Scripts/BattleArena",
            "Assets/Scripts/Player",
            "Assets/Scripts/UI",
            "Assets/Scripts/Networking",
            "Assets/Prefabs/Characters",
            "Assets/Prefabs/Vehicles",
            "Assets/Prefabs/Weapons",
            "Assets/Prefabs/Environment",
            "Assets/Materials",
            "Assets/Textures",
            "Assets/Models",
            "Assets/Audio",
            "Assets/Resources/Contracts"
        };

        foreach (string folder in folders)
        {
            if (!Directory.Exists(folder))
            {
                Directory.CreateDirectory(folder);
                Debug.Log("Created: " + folder);
            }
        }

        AssetDatabase.Refresh();
        Debug.Log("✅ Project folders created!");
    }
}
```

**Ejecutar:**
1. Guardar el archivo
2. En Unity: **Tools > Setup Project Folders**
3. Ver carpetas creadas en Project window

---

## PASO 7: Importar Scripts C# Ya Creados

### Copiar scripts desde tu proyecto actual:

```powershell
# En PowerShell, ejecutar:

# Crear carpeta destino si no existe
New-Item -ItemType Directory -Force -Path "C:\Users\Brian Carlisle\mundo virtual\unity-project\Assets\Scripts\BattleArena"

# Copiar todos los scripts C#
Copy-Item "C:\Users\Brian Carlisle\mundo virtual\unity-metaverse\Assets\Scripts\BattleArena\*.cs" `
          -Destination "C:\Users\Brian Carlisle\mundo virtual\unity-project\Assets\Scripts\BattleArena\"
```

**Scripts que se copiarán:**
- BattleArenaManager.cs
- BattlePlayer.cs
- BattleBot.cs
- BotManager.cs
- VehicleController.cs
- VehicleManager.cs
- MapGenerator.cs
- BettingSystem.cs
- DeathDropSystem.cs
- CryptoWalletSystem.cs
- RobotSuitSystem.cs
- RobotSuitShop.cs
- HiddenAccessorySystem.cs
- PlayerInventory.cs
- WeaponController.cs

### En Unity:
1. Scripts aparecerán en **Assets/Scripts/BattleArena/**
2. Esperar a que Unity compile
3. **Verificar errores en Console window** (abajo)

---

## PASO 8: Resolver Dependencias

### Si hay errores de compilación:

#### Error: "Photon not found"
**Solución:**
```
1. Asset Store (Window > Asset Store)
2. Buscar: "PUN 2 - FREE"
3. Download → Import
4. Registrarse en Photon (gratis)
5. Copiar App ID
6. Window > Photon Unity Networking > PUN Wizard
7. Pegar App ID
```

#### Error: "Using directives missing"
**Solución:**
```csharp
// Añadir al inicio de scripts:
using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using System.Collections.Generic;
```

#### Error: "Namespace 'Photon' not found"
**Esperar a instalar PUN 2** (paso anterior)

---

## PASO 9: Crear Primera Escena

### Escena: MainMenu

1. **File > New Scene**
2. Template: **Basic (URP)**
3. **File > Save As**
4. Nombre: `MainMenu`
5. Ubicación: `Assets/Scenes/MainMenu.unity`

### Añadir elementos básicos:

**Canvas (UI):**
```
Hierarchy > Right Click > UI > Canvas

Canvas Settings:
- Render Mode: Screen Space - Overlay
- UI Scale Mode: Scale With Screen Size
- Reference Resolution: 1920x1080
```

**Título del juego:**
```
Right Click en Canvas > UI > Text - TextMeshPro

Configurar:
- Text: "MUNDO VIRTUAL BATTLE ARENA"
- Font Size: 72
- Alignment: Center/Middle
- Color: White
```

**Botón Play:**
```
Right Click en Canvas > UI > Button - TextMeshPro

Configurar:
- Text: "PLAY"
- Width: 200, Height: 60
- Posición: Centro de pantalla
```

### Guardar escena:
```
Ctrl + S (guardar)
File > Build Settings > Add Open Scenes
```

---

## PASO 10: Crear Escena Battle Arena

1. **File > New Scene**
2. Template: **Basic (URP)**
3. **File > Save As** → `BattleArena.unity`

### Añadir Terrain:

```
GameObject > 3D Object > Terrain

Terrain Settings:
- Terrain Width: 5000
- Terrain Length: 5000
- Terrain Height: 600
```

### Usar ProBuilder para edificios:

```
Tools > ProBuilder > ProBuilder Window

Create Shape:
- Cube (para edificios)
- Cylinder (para torres)
- Stairs (para escaleras)
```

### Añadir Lighting:

```
Window > Rendering > Lighting

Environment:
- Skybox Material: Default (o crear custom)
- Sun Source: Directional Light

Lighting Settings:
- Realtime Global Illumination: ON
- Baked Global Illumination: ON (opcional)
```

---

## PASO 11: Crear Prefab de Player Básico

### Crear Player GameObject:

```
Hierarchy > Create Empty
Nombre: "Player"

Añadir componentes:
1. Add Component > Character Controller
   - Height: 2
   - Radius: 0.5
   
2. Add Component > Rigidbody
   - Use Gravity: YES
   - Is Kinematic: NO
   
3. Add Component > Capsule Collider (si no tiene)
```

### Añadir modelo visual temporal:

```
Right Click en Player > 3D Object > Capsule
Nombre: "PlayerModel"
Posición: (0, 1, 0)
Scale: (1, 1, 1)
```

### Añadir cámara:

```
Right Click en Player > Camera
Nombre: "PlayerCamera"
Posición: (0, 1.6, 0)
Rotation: (0, 0, 0)
```

### Crear Prefab:

```
Drag Player desde Hierarchy → Assets/Prefabs/Characters/
Ahora tienes Player.prefab
```

---

## PASO 12: Test Básico de Movimiento

### Crear script de movimiento simple:

**Assets/Scripts/Player/PlayerMovement.cs**

```csharp
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    public float moveSpeed = 5f;
    public float jumpForce = 5f;
    
    private CharacterController controller;
    private Vector3 velocity;
    private bool isGrounded;
    
    void Start()
    {
        controller = GetComponent<CharacterController>();
    }
    
    void Update()
    {
        // Check if grounded
        isGrounded = controller.isGrounded;
        
        // Get input
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        
        // Move
        Vector3 move = transform.right * horizontal + transform.forward * vertical;
        controller.Move(move * moveSpeed * Time.deltaTime);
        
        // Jump
        if (Input.GetButtonDown("Jump") && isGrounded)
        {
            velocity.y = Mathf.Sqrt(jumpForce * -2f * Physics.gravity.y);
        }
        
        // Apply gravity
        velocity.y += Physics.gravity.y * Time.deltaTime;
        controller.Move(velocity * Time.deltaTime);
        
        Debug.Log("Moving: " + move);
    }
}
```

### Añadir script al Player:
1. Seleccionar Player prefab
2. Add Component > PlayerMovement
3. Guardar (Ctrl+S)

### Test:
1. Click **Play ▶** (arriba)
2. Usar **WASD** para mover
3. **Space** para saltar
4. Ver en Console si imprime "Moving"

---

## PASO 13: Configurar Build Settings

### File > Build Settings

```
Scenes In Build:
☑ Scenes/MainMenu
☑ Scenes/BattleArena

Platform:
- PC, Mac & Linux Standalone (default)

Target Platform: Windows
Architecture: x86_64
```

### Player Settings importantes:

```
Company Name: MundoVirtual
Product Name: Battle Arena
Version: 0.1.0
Default Icon: (añadir después)

Resolution:
- Fullscreen Mode: Fullscreen Window
- Default Screen Width: 1920
- Default Screen Height: 1080
```

---

## PASO 14: Primera Build de Prueba

### Crear build ejecutable:

```
File > Build Settings
Click "Build"

Guardar en:
C:\Users\Brian Carlisle\mundo virtual\builds\windows\

Nombre: MundoVirtual_v0.1.exe
```

**Esperar 5-10 minutos** para primera build.

### Probar build:
1. Ir a carpeta builds/windows/
2. Ejecutar MundoVirtual_v0.1.exe
3. Verificar que carga MainMenu
4. Click en Play debería cargar BattleArena

---

## ✅ CHECKLIST - PROYECTO UNITY CREADO

```
☑ Unity Hub instalado
☑ Unity 2021.3 LTS instalado
☑ Proyecto "MundoVirtualBattleArena" creado
☑ URP configurado
☑ Input System instalado
☑ ProBuilder instalado
☑ Estructura de carpetas creada
☑ Scripts C# importados
☑ Scripts compilando sin errores críticos
☑ Escena MainMenu creada
☑ Escena BattleArena creada
☑ Terrain básico creado
☑ Prefab Player creado
☑ Script de movimiento funcionando
☑ Build Settings configurado
☑ Primera build ejecutable creada
```

---

## 🎯 SIGUIENTE PASO

**Ahora tienes:**
- ✅ Proyecto Unity funcional
- ✅ 2 escenas básicas
- ✅ Scripts importados
- ✅ Estructura organizada

**Próximo:**
1. Instalar Photon PUN 2 (multiplayer)
2. Importar assets 3D (personajes, armas)
3. Implementar sistema de networking
4. Conectar con blockchain

**¿Quieres que te guíe en el siguiente paso?**
- Instalar Photon PUN 2
- Descargar assets gratis
- Configurar multiplayer básico

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Unity Hub no abre
```powershell
# Reinstalar desde:
https://unity.com/download
```

### Error: "No Unity Editor installed"
```
Unity Hub > Installs > Install Editor
Versión: 2021.3 LTS
```

### Proyecto no compila
```
Window > Package Manager
Click icono ⚙ > Reset Packages to defaults
```

### Scripts con errores
```
Assets > Reimport All
Edit > Preferences > External Tools
External Script Editor: Visual Studio Community
```

### Build falla
```
File > Build Settings
Player Settings > Other Settings
Scripting Backend: IL2CPP
API Compatibility: .NET 4.x
```

---

## 📞 COMANDOS RÁPIDOS

```powershell
# Ver si Unity está instalado
Get-ChildItem "C:\Program Files\Unity\Hub\Editor"

# Crear carpeta del proyecto
New-Item -ItemType Directory -Path "C:\Users\Brian Carlisle\mundo virtual\unity-project"

# Copiar scripts
Copy-Item ".\unity-metaverse\Assets\Scripts\BattleArena\*.cs" `
          -Destination ".\unity-project\Assets\Scripts\BattleArena\" -Recurse

# Abrir proyecto en Unity (si ya existe)
Start-Process "C:\Program Files\Unity\Hub\Editor\2021.3.x\Editor\Unity.exe" `
              -ArgumentList "-projectPath `"C:\Users\Brian Carlisle\mundo virtual\unity-project`""
```
