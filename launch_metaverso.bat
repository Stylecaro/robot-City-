@echo off
title CIUDAD ROBOT METAVERSO
color 0A
cls

echo.
echo    ================================================
echo    =        CIUDAD ROBOT METAVERSO               =
echo    =              Launcher v2.0                  =
echo    ================================================
echo.

cd /d "c:\Users\Brian Carlisle\mundo virtual"

echo Verificando sistema...

:: Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no encontrado
    pause
    exit /b
)
echo OK: Python disponible

:: Iniciar Unity Hub si no esta ejecutandose
echo Iniciando Unity Hub...
tasklist /fi "imagename eq Unity Hub.exe" /fo csv 2>NUL | find /I "Unity Hub.exe" >NUL
if %errorlevel% neq 0 (
    if exist "C:\Program Files\Unity Hub\Unity Hub.exe" (
        start "" "C:\Program Files\Unity Hub\Unity Hub.exe"
        echo OK: Unity Hub iniciado
    ) else (
        echo WARNING: Unity Hub no encontrado - instalar desde unity.com
    )
) else (
    echo OK: Unity Hub ya ejecutandose
)

:: Abrir dashboard web
echo Abriendo dashboard...
if exist metaverso_dashboard.html (
    start "" metaverso_dashboard.html
    echo OK: Dashboard abierto
) else (
    echo WARNING: Dashboard no encontrado
)

:: Ejecutar sistema principal
echo Iniciando metaverso...
python quick_start.py

echo.
echo Sistema iniciado! Revisa Unity Hub y el navegador
echo.
pause