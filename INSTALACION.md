# Instalación y Configuración - Metaverso Professional

## 🔧 Guía de Instalación Rápida

### 1. Requisitos del Sistema
- Python 3.10+ (Probado con Python 3.13.5)
- Windows 10/11 (Compatible con PowerShell)
- 4GB RAM mínimo (8GB recomendado)
- 1GB espacio libre en disco

### 2. Instalación de Dependencias
```bash
# Configurar entorno Python
pip install --upgrade pip
pip install Flask Flask-CORS psutil

# Verificar instalación
python -c "import flask, flask_cors, psutil; print('✅ Dependencias instaladas correctamente')"
```

### 3. Ejecución del Sistema
```bash
# Navegar al directorio del proyecto
cd "C:\Users\Brian Carlisle\mundo virtual"

# Iniciar servidor profesional
python metaverso_professional.py
```

### 4. Acceso al Sistema
- **Dashboard Principal**: http://127.0.0.1:5000
- **API Status**: http://127.0.0.1:5000/api/status
- **API Metrics**: http://127.0.0.1:5000/api/metrics
- **Health Check**: http://127.0.0.1:5000/api/health

## 🚀 Scripts de Inicio Automático

### Windows PowerShell Script
```powershell
# inicio_metaverso.ps1
Set-Location "C:\Users\Brian Carlisle\mundo virtual"
Write-Host "🚀 Iniciando Metaverso Professional..." -ForegroundColor Green
python metaverso_professional.py
```

### Batch File
```batch
@echo off
cd "C:\Users\Brian Carlisle\mundo virtual"
echo 🚀 Iniciando Metaverso Professional...
python metaverso_professional.py
pause
```

## 📊 Monitoreo y Logs

### Archivos de Log
- **Ubicación**: `metaverso_professional.log`
- **Codificación**: UTF-8
- **Rotación**: Manual (recomendado cada 100MB)

### Comandos de Monitoreo
```bash
# Ver logs en tiempo real
Get-Content -Path "metaverso_professional.log" -Wait

# Verificar estado del servidor
curl http://127.0.0.1:5000/api/health
```

## 🔧 Solución de Problemas

### Error: No module named 'flask'
```bash
pip install Flask Flask-CORS psutil
```

### Error: UnicodeEncodeError
- ✅ **Solucionado**: El sistema profesional maneja UTF-8 correctamente
- Los logs no contienen emojis problemáticos

### Puerto 5000 ocupado
```bash
# Verificar procesos en el puerto
netstat -ano | findstr :5000

# Terminar proceso si es necesario
taskkill /F /PID [PID_NUMBER]
```

### Sistema no responde
```bash
# Reiniciar servidor limpiamente
taskkill /F /IM python.exe /T
python metaverso_professional.py
```

## 🎯 Verificación de Funcionamiento

### Checklist de Validación
- [ ] Servidor inicia sin errores
- [ ] Dashboard carga en http://127.0.0.1:5000
- [ ] APIs responden correctamente
- [ ] Métricas se actualizan en tiempo real
- [ ] Logs se generan correctamente
- [ ] Sistema responde a interrupciones (Ctrl+C)

### Comandos de Validación
```bash
# Verificar servidor activo
curl -s http://127.0.0.1:5000/api/health | python -m json.tool

# Verificar métricas
curl -s http://127.0.0.1:5000/api/metrics | python -m json.tool

# Verificar estado del sistema
curl -s http://127.0.0.1:5000/api/status | python -m json.tool
```

---

**Sistema preparado para uso profesional** ✅