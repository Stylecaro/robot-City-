@echo off
title Metaverso Ciudad Robot - Lanzador
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║     🤖 METAVERSO CIUDAD ROBOT - SISTEMA COMPLETO IA 🌟     ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🚀 Iniciando sistema...
echo.

cd /d "%~dp0"

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    echo Por favor instala Python 3.9+ desde python.org
    pause
    exit /b 1
)

echo ✅ Python detectado
echo.

REM Instalar dependencias si es necesario
echo 📦 Verificando dependencias...
pip install -q numpy tensorflow torch fastapi uvicorn websockets scikit-learn pandas aiohttp 2>nul

echo.
echo ✅ Dependencias verificadas
echo.
echo 🌐 Iniciando servidor backend...
echo    Dashboard: http://localhost:8765
echo    API: http://localhost:8765/api/status
echo.
echo Presiona Ctrl+C para detener
echo.

REM Ejecutar servidor
python metaverso_integrated_server.py

pause
