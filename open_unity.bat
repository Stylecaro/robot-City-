@echo off
title Abrir Unity Hub - Ciudad Robot Metaverso
color 0B

echo.
echo ================================================================
echo                    ABRIENDO UNITY HUB
echo                 Ciudad Robot Metaverso
echo ================================================================
echo.

echo 🎮 Buscando Unity Hub...

:: Verificar rutas comunes de Unity Hub
set UNITY_HUB_PATH=""

if exist "C:\Program Files\Unity Hub\Unity Hub.exe" (
    set UNITY_HUB_PATH="C:\Program Files\Unity Hub\Unity Hub.exe"
    echo ✅ Unity Hub encontrado en Program Files
) else if exist "C:\Program Files (x86)\Unity Hub\Unity Hub.exe" (
    set UNITY_HUB_PATH="C:\Program Files (x86)\Unity Hub\Unity Hub.exe"
    echo ✅ Unity Hub encontrado en Program Files (x86)
) else (
    echo ❌ Unity Hub no encontrado en rutas estándar
    echo 📥 Abriendo página de descarga...
    start https://unity.com/download
    goto END
)

echo 🚀 Iniciando Unity Hub...
start "" %UNITY_HUB_PATH%

echo ✅ Unity Hub iniciado correctamente
echo.
echo 📋 SIGUIENTE PASO - En Unity Hub:
echo    1. Instalar Unity Editor 2022.3 LTS (recomendado)
echo    2. Crear nuevo proyecto 3D
echo    3. Nombre: "CiudadRobotMetaverso"
echo    4. Ubicación: "c:\Users\Brian Carlisle\mundo virtual\UnityProject"
echo.
echo 🌟 ¡Listo para explorar el metaverso!

:END
pause
echo Presiona cualquier tecla para continuar...