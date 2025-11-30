# 🤖 METAVERSO CIUDAD ROBOT - GUÍA RÁPIDA

## 🎯 INICIO RÁPIDO (3 PASOS)

### 1. Ejecutar Backend
```bash
# Doble click en:
INICIAR_METAVERSO.bat

# O ejecutar manualmente:
python metaverso_integrated_server.py
```

**Se abrirá automáticamente:**
- ✅ Dashboard web en http://localhost:8765
- ✅ AI Coordinator con 10 robots
- ✅ Predictive Analytics Engine
- ✅ WebSocket Server

### 2. Abrir Unity
1. Abrir Unity Hub
2. Add → `UnityProject/`
3. Abrir proyecto
4. Esperar carga (1-2 min)

### 3. Configurar Unity
1. **Crear NetworkManager:**
   - GameObject → Create Empty
   - Nombre: "NetworkManager"
   - Add Component → **NetworkManager**
   - Server URL: `ws://localhost:8765`

2. **Crear CityManager:**
   - GameObject → Create Empty
   - Nombre: "CityManager"
   - Add Component → **CityManager**
   - Robot Prefab: (Opcional - deja en None)

3. **Presionar PLAY ▶️**

---

## ✅ VERIFICAR QUE FUNCIONA

### Backend (Python):
- ✅ Terminal muestra: `"✅ Servidor corriendo en http://0.0.0.0:8765"`
- ✅ Dashboard web carga correctamente
- ✅ "Estado del Sistema" muestra robots activos

### Unity:
- ✅ Console muestra: `"🌐 Conectando a ws://localhost:8765..."`
- ✅ Console muestra: `"✅ Conectado al servidor"`
- ✅ Scene View muestra 4 edificios y robots moviéndose
- ✅ Game View muestra la ciudad en 3D

### Dashboard Web:
- ✅ "Clientes Unity: 1" (después de conectar Unity)
- ✅ "Robots Totales" aumenta con el tiempo
- ✅ Métricas se actualizan cada 5 segundos
- ✅ Recomendaciones aparecen en pantalla

---

## 🎮 CONTROLES

### Dashboard Web:
- **➕ Crear Robot Manufactura** - Spawn nuevo robot azul
- **➕ Crear Robot Investigación** - Spawn nuevo robot verde
- **➕ Crear Robot Seguridad** - Spawn nuevo robot rojo
- **🔄 Actualizar** - Refrescar métricas manualmente

### Unity:
- **WASD** - Mover cámara (si tienes CharacterController)
- **Mouse** - Rotar vista
- **F** - Focus en objeto seleccionado
- **Scene View** - Ver robots desde arriba

---

## 📊 QUÉ VER EN EL DASHBOARD

### Estado del Sistema:
- **🟢 Activo** - Sistema operativo
- **Robots Totales** - Cantidad de robots creados
- **Robots Activos** - Robots trabajando/patrullando
- **Clientes Unity** - Instancias de Unity conectadas

### Inteligencia Artificial:
- **Modelo Entrenado** - ✅ Sí / ⏳ No
- **Métricas Recopiladas** - Datos históricos (más = mejor predicción)
- **Eficiencia Manufactura** - 0-100% (promedio batería robots azules)
- **Barra de progreso** - Visual de eficiencia

### Análisis Predictivo:
- **Predicción Tráfico** - Congestión futura (0-100%)
- **Predicción Energía** - Consumo previsto próxima hora
- **Confianza** - Precisión de predicción (>60% = confiable)

### Alertas Activas:
- **🚨 CRITICAL** - Requiere acción inmediata
- **⚠️ HIGH** - Atención necesaria pronto
- **⚡ MEDIUM** - Monitorear
- **ℹ️ LOW** - Informativo

### Recomendaciones:
- **🚦 Tráfico** - Redistribuir robots, crear rutas
- **⚡ Energía** - Enviar a carga, modo ahorro
- **🔧 Mantenimiento** - Programar reparaciones
- **✅ Todo OK** - Sistemas óptimos

---

## 🤖 COMPORTAMIENTO DE ROBOTS

### Estados Visuales:
- **🟢 Verde** - IDLE (esperando tareas)
- **🟡 Amarillo** - WORKING/PATROL (activo)
- **🔵 Azul** - CHARGING (recargando batería)
- **🔴 Rojo** - EMERGENCY (batería/salud crítica)

### Comportamientos Automáticos:
1. **Patrullar** - Se mueven aleatoriamente
2. **Trabajar** - Van a posición de tarea
3. **Cargar** - Buscan estación más cercana si batería < 20%
4. **Emergencia** - Fuerzan carga/reparación si críticos

### Degradación:
- **Batería** - Disminuye 0.01/seg trabajando
- **Salud** - Disminuye 0.001/seg en uso
- **Auto-reparación** - +0.02/seg en mantenimiento

---

## 🏗️ EDIFICIOS EN LA CIUDAD

### 1. Manufacturing Center (Azul - SO)
- Posición: (-40, 0, -40)
- Tamaño: 30x60x30
- Función: Producción de componentes

### 2. Research Lab (Verde - SE)
- Posición: (40, 0, -40)
- Tamaño: 25x80x25
- Función: Investigación y desarrollo

### 3. Security HQ (Rojo - NO)
- Posición: (-40, 0, 40)
- Tamaño: 35x50x35
- Función: Control de seguridad

### 4. AI Core (Amarillo - NE)
- Posición: (40, 0, 40)
- Tamaño: 40x100x40
- Función: Centro de inteligencia artificial

### 5. Estaciones de Carga (Cyan - 4x)
- Posición: Norte, Sur, Este, Oeste (60m del centro)
- Tag: "ChargeStation"
- Función: Recargar batería de robots

### 6. Plaza Central (Gris)
- Posición: (0, 0, 0)
- Diámetro: 80m
- Función: Área de circulación

---

## 🔧 PROBLEMAS COMUNES

### "No se conecta Unity"
**Solución:**
1. Verificar que backend esté corriendo
2. En Unity Console buscar errores
3. Verificar URL en NetworkManager: `ws://localhost:8765`
4. Reiniciar Unity

### "No aparecen robots"
**Solución:**
1. Verificar que CityManager esté en la escena
2. Verificar que autoSpawnRobots = true
3. Esperar 5-10 segundos
4. Revisar Hierarchy para ver "Robots" parent

### "Dashboard dice 'Desconectado'"
**Solución:**
1. Verificar que el backend esté corriendo
2. Abrir http://localhost:8765 manualmente
3. Revisar firewall de Windows
4. Ejecutar como Administrador

### "Predicciones siempre 0%"
**Solución:**
1. Esperar 10+ minutos para recopilar datos
2. Verificar instalación: `pip install scikit-learn`
3. Revisar logs del servidor

---

## 📈 OPTIMIZACIÓN

### Aumentar Rendimiento Unity:
```
Edit → Project Settings → Quality
- Shadows: Disable
- Anti Aliasing: Disabled
- V Sync: Off
```

### Reducir Uso de CPU:
```csharp
// En CityManager.cs, cambiar:
InvokeRepeating(nameof(SyncWithAI), 1f, 10f);  // De 5s a 10s
```

### Más Robots:
```csharp
// En CityManager.cs:
public int maxRobots = 500;  // De 200 a 500
```

---

## 🎯 PRUEBAS RECOMENDADAS

### Test 1: Spawn Masivo
1. En dashboard, click 10 veces "Crear Robot"
2. Ver que Unity los muestra
3. Verificar métricas actualizadas

### Test 2: Batería Crítica
1. En Unity, seleccionar un robot
2. En Inspector, cambiar Battery Level a 0.1
3. Ver que va automáticamente a estación de carga

### Test 3: Predicciones
1. Dejar sistema corriendo 15 minutos
2. Refrescar dashboard
3. Ver predicciones con confianza >70%

### Test 4: Alertas
1. En Unity, poner Health de robot a 0.2
2. Ver alerta de mantenimiento en dashboard
3. Ver recomendación de reparación

---

## 🌟 SIGUIENTE NIVEL

### Mejorar Visuales:
1. Window → Package Manager
2. Instalar "Universal RP"
3. Edit → Project Settings → Graphics → URP High
4. Assets → Create → Rendering → URP Asset

### Añadir Sonidos:
1. Importar audio clips
2. Añadir AudioSource a robots
3. Play sound en eventos (spawn, charge, etc.)

### Crear Tareas Personalizadas:
```python
# En dashboard o API:
POST /api/assign_task
{
  "robot_id": "manufacturing_123",
  "task": {
    "x": 50, "y": 0, "z": 50,
    "priority": "HIGH"
  }
}
```

---

**✅ ¡SISTEMA LISTO PARA USAR!**

Ejecuta `INICIAR_METAVERSO.bat` → Abre Unity → PLAY ▶️
