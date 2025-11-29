@echo off
title Unity Hub - Ciudad Robot Metaverso
color 0A
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║           🎮 UNITY HUB - METAVERSO LAUNCHER 🌆              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🔍 Verificando Unity Hub...

tasklist /FI "IMAGENAME eq Unity Hub.exe" 2>NUL | find /I /N "Unity Hub.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo ✅ Unity Hub está ejecutándose
) else (
    echo ❌ Unity Hub no está ejecutándose
    echo 🔄 Intentando abrir Unity Hub...
    start "" "unityhub:///"
    timeout /t 3 /nobreak >nul
)

echo.
echo 📋 OPCIONES DISPONIBLES:
echo.
echo 1. 🎮 Abrir Unity Hub (si no está abierto)
echo 2. 📂 Abrir carpeta del proyecto Unity
echo 3. 🌐 Abrir dashboard web del metaverso  
echo 4. 📖 Ver guía completa de Unity Hub
echo 5. 🚀 Ejecutar launcher completo del metaverso
echo 6. ❌ Salir
echo.

:menu
set /p choice="Selecciona una opción (1-6): "

if "%choice%"=="1" (
    echo 🎮 Abriendo Unity Hub...
    start "" "unityhub:///"
    timeout /t 2 /nobreak >nul
    goto menu
)

if "%choice%"=="2" (
    echo 📂 Abriendo carpeta del proyecto...
    explorer "UnityProject"
    goto menu
)

if "%choice%"=="3" (
    echo 🌐 Abriendo dashboard web...
    start "" "http://localhost:8000"
    goto menu
)

if "%choice%"=="4" (
    echo 📖 Mostrando guía completa...
    python unity_hub_guide.py
    pause
    goto menu
)

if "%choice%"=="5" (
    echo 🚀 Ejecutando launcher completo...
    python metaverso_launcher.py
    goto menu
)

if "%choice%"=="6" (
    echo 👋 ¡Hasta luego!
    exit
)

echo ❌ Opción no válida. Por favor selecciona 1-6.
goto menu