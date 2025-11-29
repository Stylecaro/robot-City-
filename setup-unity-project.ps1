# Script PowerShell para crear proyecto Unity automáticamente
# Autor: GitHub Copilot para Mundo Virtual

Write-Host "🚀 CREANDO PROYECTO UNITY AUTOMÁTICAMENTE..." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# Variables
$projectPath = "C:\Users\Brian Carlisle\mundo virtual\unity-project"
$unityHubPath = "C:\Program Files\Unity Hub\Unity Hub.exe"
$scriptsSource = "C:\Users\Brian Carlisle\mundo virtual\unity-metaverse\Assets\Scripts\BattleArena"

# Paso 1: Verificar si Unity Hub está instalado
Write-Host "`n[1/10] Verificando Unity Hub..." -ForegroundColor Yellow

if (Test-Path $unityHubPath) {
    Write-Host "✅ Unity Hub encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ Unity Hub no encontrado" -ForegroundColor Red
    Write-Host "`nDescargando Unity Hub..." -ForegroundColor Yellow
    
    $hubUrl = "https://public-cdn.cloud.unity3d.com/hub/prod/UnityHubSetup.exe"
    $hubInstaller = "$env:TEMP\UnityHubSetup.exe"
    
    try {
        Invoke-WebRequest -Uri $hubUrl -OutFile $hubInstaller
        Write-Host "✅ Unity Hub descargado" -ForegroundColor Green
        Write-Host "Ejecutando instalador..." -ForegroundColor Yellow
        Start-Process $hubInstaller -Wait
        Write-Host "✅ Unity Hub instalado" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error al descargar Unity Hub" -ForegroundColor Red
        Write-Host "Por favor descarga manualmente desde: https://unity.com/download" -ForegroundColor Yellow
        exit
    }
}

# Paso 2: Verificar Unity Editor instalado
Write-Host "`n[2/10] Verificando Unity Editor..." -ForegroundColor Yellow

$editorPath = "C:\Program Files\Unity\Hub\Editor"
if (Test-Path $editorPath) {
    $versions = Get-ChildItem $editorPath -Directory | Select-Object -ExpandProperty Name
    if ($versions.Count -gt 0) {
        Write-Host "✅ Unity Editor encontrado: $($versions[0])" -ForegroundColor Green
        $unityExe = Join-Path $editorPath "$($versions[0])\Editor\Unity.exe"
    } else {
        Write-Host "⚠️ No hay versiones de Unity instaladas" -ForegroundColor Yellow
        Write-Host "Por favor instala Unity 2021.3 LTS desde Unity Hub" -ForegroundColor Yellow
        Write-Host "Abriendo Unity Hub..." -ForegroundColor Yellow
        Start-Process $unityHubPath
        exit
    }
} else {
    Write-Host "⚠️ Unity Editor no encontrado" -ForegroundColor Yellow
    Write-Host "Por favor instala Unity 2021.3 LTS desde Unity Hub" -ForegroundColor Yellow
    Write-Host "Abriendo Unity Hub..." -ForegroundColor Yellow
    Start-Process $unityHubPath
    exit
}

# Paso 3: Crear carpeta del proyecto
Write-Host "`n[3/10] Creando estructura del proyecto..." -ForegroundColor Yellow

if (Test-Path $projectPath) {
    Write-Host "⚠️ El proyecto ya existe en $projectPath" -ForegroundColor Yellow
    $response = Read-Host "¿Deseas sobrescribirlo? (s/n)"
    if ($response -ne 's') {
        Write-Host "❌ Operación cancelada" -ForegroundColor Red
        exit
    }
    Remove-Item $projectPath -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $projectPath | Out-Null
Write-Host "✅ Carpeta de proyecto creada" -ForegroundColor Green

# Paso 4: Crear estructura de carpetas
Write-Host "`n[4/10] Creando estructura de carpetas..." -ForegroundColor Yellow

$folders = @(
    "Assets\Scenes",
    "Assets\Scripts\BattleArena",
    "Assets\Scripts\Player",
    "Assets\Scripts\UI",
    "Assets\Scripts\Networking",
    "Assets\Prefabs\Characters",
    "Assets\Prefabs\Vehicles",
    "Assets\Prefabs\Weapons",
    "Assets\Prefabs\Environment",
    "Assets\Materials",
    "Assets\Textures",
    "Assets\Models",
    "Assets\Audio",
    "Assets\Resources\Contracts"
)

foreach ($folder in $folders) {
    $fullPath = Join-Path $projectPath $folder
    New-Item -ItemType Directory -Force -Path $fullPath | Out-Null
}

Write-Host "✅ Estructura de carpetas creada" -ForegroundColor Green

# Paso 5: Copiar scripts C# si existen
Write-Host "`n[5/10] Copiando scripts C#..." -ForegroundColor Yellow

if (Test-Path $scriptsSource) {
    $destScripts = Join-Path $projectPath "Assets\Scripts\BattleArena"
    Copy-Item "$scriptsSource\*.cs" -Destination $destScripts -Force
    $scriptCount = (Get-ChildItem $destScripts -Filter "*.cs").Count
    Write-Host "✅ $scriptCount scripts copiados" -ForegroundColor Green
} else {
    Write-Host "⚠️ Scripts fuente no encontrados en $scriptsSource" -ForegroundColor Yellow
    Write-Host "Los scripts se crearán después en Unity" -ForegroundColor Yellow
}

# Paso 6: Crear archivo de configuración del proyecto
Write-Host "`n[6/10] Creando archivos de configuración..." -ForegroundColor Yellow

# ProjectSettings básicos
$projectSettingsPath = Join-Path $projectPath "ProjectSettings"
New-Item -ItemType Directory -Force -Path $projectSettingsPath | Out-Null

# ProjectVersion.txt
$projectVersion = @"
m_EditorVersion: 2021.3.0f1
m_EditorVersionWithRevision: 2021.3.0f1 (1234567890ab)
"@
$projectVersion | Out-File -FilePath (Join-Path $projectSettingsPath "ProjectVersion.txt") -Encoding UTF8

Write-Host "✅ Archivos de configuración creados" -ForegroundColor Green

# Paso 7: Crear script de movimiento básico
Write-Host "`n[7/10] Creando script PlayerMovement.cs..." -ForegroundColor Yellow

$playerMovementScript = @"
using UnityEngine;

public class PlayerMovement : MonoBehaviour
{
    [Header("Movement Settings")]
    public float moveSpeed = 5f;
    public float jumpForce = 5f;
    public float mouseSensitivity = 2f;
    
    [Header("References")]
    public Transform playerCamera;
    
    private CharacterController controller;
    private Vector3 velocity;
    private float xRotation = 0f;
    
    void Start()
    {
        controller = GetComponent<CharacterController>();
        Cursor.lockState = CursorLockMode.Locked;
        
        if (playerCamera == null)
        {
            playerCamera = Camera.main.transform;
        }
    }
    
    void Update()
    {
        // Mouse look
        float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity;
        float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity;
        
        xRotation -= mouseY;
        xRotation = Mathf.Clamp(xRotation, -90f, 90f);
        
        playerCamera.localRotation = Quaternion.Euler(xRotation, 0f, 0f);
        transform.Rotate(Vector3.up * mouseX);
        
        // Movement
        float horizontal = Input.GetAxis("Horizontal");
        float vertical = Input.GetAxis("Vertical");
        
        Vector3 move = transform.right * horizontal + transform.forward * vertical;
        controller.Move(move * moveSpeed * Time.deltaTime);
        
        // Jump
        if (Input.GetButtonDown("Jump") && controller.isGrounded)
        {
            velocity.y = Mathf.Sqrt(jumpForce * -2f * Physics.gravity.y);
        }
        
        // Gravity
        if (!controller.isGrounded)
        {
            velocity.y += Physics.gravity.y * Time.deltaTime;
        }
        else if (velocity.y < 0)
        {
            velocity.y = -2f;
        }
        
        controller.Move(velocity * Time.deltaTime);
    }
}
"@

$playerScriptPath = Join-Path $projectPath "Assets\Scripts\Player\PlayerMovement.cs"
$playerMovementScript | Out-File -FilePath $playerScriptPath -Encoding UTF8

Write-Host "✅ PlayerMovement.cs creado" -ForegroundColor Green

# Paso 8: Crear README del proyecto
Write-Host "`n[8/10] Creando README..." -ForegroundColor Yellow

$readme = @"
# Mundo Virtual - Battle Arena
## Unity Project

### Estructura del Proyecto

- **Assets/Scenes/** - Escenas del juego
- **Assets/Scripts/** - Scripts C#
- **Assets/Prefabs/** - Prefabs reutilizables
- **Assets/Materials/** - Materiales y shaders
- **Assets/Models/** - Modelos 3D

### Cómo Abrir el Proyecto

1. Abrir Unity Hub
2. Click en "Add" o "Open"
3. Seleccionar esta carpeta: $projectPath
4. Unity abrirá el proyecto automáticamente

### Requisitos

- Unity 2021.3 LTS o superior
- Visual Studio 2022
- Photon PUN 2 (instalado desde Asset Store)

### Próximos Pasos

1. Instalar Photon PUN 2 desde Asset Store
2. Importar assets 3D
3. Configurar escenas
4. Conectar con blockchain (backend Python)

### Scripts Disponibles

- PlayerMovement.cs - Movimiento básico del jugador
- BattleArenaManager.cs - Gestión de arena
- BotManager.cs - Sistema de bots AI
- VehicleController.cs - Control de vehículos
- RobotSuitSystem.cs - Sistema de trajes
- Y más...

### Contacto

Proyecto: Mundo Virtual Battle Arena
Fecha: $(Get-Date -Format "dd/MM/yyyy")
"@

$readme | Out-File -FilePath (Join-Path $projectPath "README.md") -Encoding UTF8

Write-Host "✅ README.md creado" -ForegroundColor Green

# Paso 9: Crear script de instalación de packages
Write-Host "`n[9/10] Creando manifest de packages..." -ForegroundColor Yellow

$packagesPath = Join-Path $projectPath "Packages"
New-Item -ItemType Directory -Force -Path $packagesPath | Out-Null

$manifest = @"
{
  "dependencies": {
    "com.unity.collab-proxy": "2.0.5",
    "com.unity.feature.development": "1.0.1",
    "com.unity.inputsystem": "1.5.1",
    "com.unity.probuilder": "5.0.7",
    "com.unity.render-pipelines.universal": "12.1.11",
    "com.unity.textmeshpro": "3.0.6",
    "com.unity.timeline": "1.6.5",
    "com.unity.ugui": "1.0.0",
    "com.unity.visualscripting": "1.8.0",
    "com.unity.modules.ai": "1.0.0",
    "com.unity.modules.androidjni": "1.0.0",
    "com.unity.modules.animation": "1.0.0",
    "com.unity.modules.assetbundle": "1.0.0",
    "com.unity.modules.audio": "1.0.0",
    "com.unity.modules.cloth": "1.0.0",
    "com.unity.modules.director": "1.0.0",
    "com.unity.modules.imageconversion": "1.0.0",
    "com.unity.modules.imgui": "1.0.0",
    "com.unity.modules.jsonserialize": "1.0.0",
    "com.unity.modules.particlesystem": "1.0.0",
    "com.unity.modules.physics": "1.0.0",
    "com.unity.modules.physics2d": "1.0.0",
    "com.unity.modules.screencapture": "1.0.0",
    "com.unity.modules.terrain": "1.0.0",
    "com.unity.modules.terrainphysics": "1.0.0",
    "com.unity.modules.tilemap": "1.0.0",
    "com.unity.modules.ui": "1.0.0",
    "com.unity.modules.uielements": "1.0.0",
    "com.unity.modules.umbra": "1.0.0",
    "com.unity.modules.unityanalytics": "1.0.0",
    "com.unity.modules.unitywebrequest": "1.0.0",
    "com.unity.modules.unitywebrequestassetbundle": "1.0.0",
    "com.unity.modules.unitywebrequestaudio": "1.0.0",
    "com.unity.modules.unitywebrequesttexture": "1.0.0",
    "com.unity.modules.unitywebrequestwww": "1.0.0",
    "com.unity.modules.vehicles": "1.0.0",
    "com.unity.modules.video": "1.0.0",
    "com.unity.modules.vr": "1.0.0",
    "com.unity.modules.wind": "1.0.0",
    "com.unity.modules.xr": "1.0.0"
  }
}
"@

$manifest | Out-File -FilePath (Join-Path $packagesPath "manifest.json") -Encoding UTF8

Write-Host "✅ Manifest de packages creado" -ForegroundColor Green

# Paso 10: Abrir proyecto en Unity
Write-Host "`n[10/10] Preparando para abrir Unity..." -ForegroundColor Yellow

Write-Host "`n✅ ¡PROYECTO CREADO EXITOSAMENTE!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "`nUbicación: $projectPath" -ForegroundColor White
Write-Host "`nPara abrir el proyecto:" -ForegroundColor Yellow
Write-Host "1. Abre Unity Hub" -ForegroundColor White
Write-Host "2. Click en 'Add' o 'Open'" -ForegroundColor White
Write-Host "3. Selecciona la carpeta: $projectPath" -ForegroundColor White
Write-Host "`n¿Deseas abrir Unity Hub ahora? (s/n): " -ForegroundColor Yellow -NoNewline

$openHub = Read-Host

if ($openHub -eq 's') {
    Write-Host "`nAbriendo Unity Hub..." -ForegroundColor Yellow
    Start-Process $unityHubPath
    Start-Sleep -Seconds 2
    
    Write-Host "`nAhora en Unity Hub:" -ForegroundColor Cyan
    Write-Host "1. Click en 'Open' o 'Add'" -ForegroundColor White
    Write-Host "2. Navega a: $projectPath" -ForegroundColor White
    Write-Host "3. Unity abrirá y configurará el proyecto automáticamente" -ForegroundColor White
    Write-Host "4. Espera 5-10 minutos la primera vez" -ForegroundColor Yellow
}

Write-Host "`n📋 RESUMEN:" -ForegroundColor Cyan
Write-Host "✅ Estructura de carpetas creada" -ForegroundColor Green
Write-Host "✅ Scripts C# copiados" -ForegroundColor Green
Write-Host "✅ PlayerMovement.cs creado" -ForegroundColor Green
Write-Host "✅ Packages manifest configurado" -ForegroundColor Green
Write-Host "✅ README.md incluido" -ForegroundColor Green

Write-Host "`n🎯 PRÓXIMOS PASOS:" -ForegroundColor Cyan
Write-Host "1. Abrir proyecto en Unity Hub" -ForegroundColor White
Write-Host "2. Esperar que Unity importe packages (~10 min)" -ForegroundColor White
Write-Host "3. Crear primera escena (MainMenu)" -ForegroundColor White
Write-Host "4. Instalar Photon PUN 2 desde Asset Store" -ForegroundColor White
Write-Host "5. Importar assets 3D" -ForegroundColor White

Write-Host "`n🚀 ¡Todo listo para empezar!" -ForegroundColor Green
