# Sistema de Bots AI y Vehículos de Combate

## 🤖 Bots Inteligentes

### Tipos de Bots

1. **Humanoide Bot**
   - Salud: 100 HP
   - Velocidad: 5 m/s
   - Rango de detección: 40m
   - Precisión: 60-90% (según skill level)
   - Comportamiento: Patrulla, caza, ataque básico

2. **Terminator**
   - Salud: 200 HP + 50 armor
   - Velocidad: 4 m/s
   - Rango de detección: 60m
   - Precisión: 80-100%
   - Tiempo de reacción: 0.2s
   - Comportamiento: Agresivo, persiste en combate

3. **Dron de Combate**
   - Salud: 75 HP
   - Velocidad: 8 m/s (vuela)
   - Rango de detección: 70m
   - Precisión: 90%
   - Tiempo de reacción: 0.1s
   - Comportamiento: Vuelo táctico, ataque desde altura

### Estados de IA
```
PATROL → Patrulla aleatoria en NavMesh
HUNT → Persigue enemigo detectado
ATTACK → Combate activo con enemigo
RETREAT → Huye cuando tiene <30% HP
LOOT_SEARCH → Busca loot boxes y armas
```

### Características de IA

- **Detección inteligente**: Sphere overlap con rango configurable
- **Pathfinding**: Unity NavMesh para movimiento natural
- **Aim con imprecisión**: Spread basado en skill level
- **Toma de decisiones**: State machine con prioridades
- **Loot**: Bots dropean 10-50 EVT al morir
- **Auto-fill**: Sistema de llenado automático de partidas

## 🚗 Vehículos de Combate

### Tipos de Vehículos

1. **Tanque de Combate** 🛡️
   - Salud: 1000 HP
   - Velocidad: 15 m/s
   - Daño: 100 por disparo
   - Cadencia: 1 disparo/s
   - Pasajeros: 2 (conductor + artillero)
   - Ventaja: Alta resistencia y daño

2. **Auto Blindado** 🚙
   - Salud: 300 HP
   - Velocidad: 40 m/s
   - Daño: 30 por disparo
   - Cadencia: 5 disparos/s
   - Pasajeros: 4 (equipo completo)
   - Ventaja: Velocidad y movilidad

3. **Dron de Ataque** 🛸
   - Salud: 200 HP
   - Velocidad: 50 m/s
   - Daño: 25 por disparo
   - Cadencia: 10 disparos/s
   - Pasajeros: 1 (piloto)
   - Ventaja: Vuelo, difícil de golpear

4. **Mech Destructor** 🤖
   - Salud: 1500 HP
   - Velocidad: 10 m/s
   - Daño: 150 por disparo
   - Cadencia: 0.5 disparos/s
   - Pasajeros: 1 (piloto)
   - Ventaja: Tanque humanoide con armas pesadas

5. **Excavadora Armada** 🚜
   - Salud: 800 HP
   - Velocidad: 8 m/s
   - Daño: 200 (cuerpo a cuerpo)
   - Cadencia: 2 ataques/s
   - Pasajeros: 1 (operador)
   - Ventaja: Destruye edificios y terreno

### Mecánicas de Vehículos

#### Entrada/Salida
```csharp
// Presionar F cerca del vehículo para subir
Input.GetKeyDown(KeyCode.F) → EnterVehicle()

// Presionar F mientras conduces para salir
Input.GetKeyDown(KeyCode.F) → ExitVehicle()
```

#### Controles
- **W/S**: Acelerar/Retroceder
- **A/D**: Girar
- **Mouse**: Apuntar torreta (tanque/mech)
- **Click Izquierdo**: Disparar
- **F**: Entrar/Salir

#### Sistema de Daño
- Vehículos tienen HP separado del jugador
- Al destruirse, expulsan a todos los pasajeros
- Explosión final causa 100 HP de daño en 10m de radio
- Vehículos pueden dañarse entre sí

#### Spawn System
- Spawns fijos en el mapa (10 puntos)
- Respawn automático después de 60 segundos
- Tipos de vehículos aleatorios
- Sincronización Photon para multiplayer

## 🎮 Integración con Sistema Existente

### Conexión con Economía EVT

**Recompensas por Kills con Vehículos:**
```python
# Python backend
def calculate_vehicle_kill_reward(vehicle_type):
    base_reward = 25  # EVT base
    multipliers = {
        "CombatTank": 2.0,      # 50 EVT
        "ArmoredCar": 1.5,      # 37.5 EVT
        "AttackDrone": 1.8,     # 45 EVT
        "DestroyerMech": 2.5,   # 62.5 EVT
        "Excavator": 2.2        # 55 EVT
    }
    return base_reward * multipliers.get(vehicle_type, 1.0)
```

**Penalización por Destrucción:**
- Perder vehículo: -10 EVT (reparación)
- Destruir vehículo enemigo: +50 EVT (bonus)

### Integración con Betting System

```csharp
// BettingSystem.cs - Modificación
public void CalculateVehicleBonus(VehicleType vehicleUsed)
{
    float bonus = 1.0f;
    
    switch (vehicleUsed)
    {
        case VehicleType.DestroyerMech:
            bonus = 1.5f; // 50% bonus por usar mech
            break;
        case VehicleType.Excavator:
            bonus = 1.3f; // 30% bonus por excavadora
            break;
    }
    
    currentPrizePool *= bonus;
}
```

### Integración con Death Drop

```csharp
// DeathDropSystem.cs
public void HandleVehicleDestruction(VehicleController vehicle)
{
    // Crear loot box con ammo del vehículo
    GameObject lootBox = CreateLootBox(vehicle.transform.position);
    
    LootBox loot = lootBox.GetComponent<LootBox>();
    loot.ammoAmount = vehicle.currentAmmo;
    loot.tokenAmount = Random.Range(20f, 100f); // EVT tokens
    loot.weaponType = vehicle.vehicleType.ToString();
}
```

## 📊 Configuración JSON

Añadir a `game_modes_config.json`:

```json
{
  "ai_bots": {
    "enabled": true,
    "auto_fill": true,
    "max_bots": 50,
    "skill_levels": {
      "casual": 0.3,
      "ranked": 0.6,
      "tournament": 0.8,
      "high_stakes": 0.9
    },
    "bot_types": {
      "humanoid": 0.6,
      "terminator": 0.3,
      "combat_drone": 0.1
    },
    "loot_drop": {
      "min_tokens": 10,
      "max_tokens": 50,
      "drop_weapons": true
    }
  },
  
  "vehicles": {
    "enabled": true,
    "max_vehicles": 10,
    "respawn_time": 60,
    "spawn_distribution": {
      "combat_tank": 0.15,
      "armored_car": 0.35,
      "attack_drone": 0.20,
      "destroyer_mech": 0.10,
      "excavator": 0.20
    },
    "rewards": {
      "vehicle_kill_bonus": 50,
      "vehicle_destruction_penalty": -10,
      "multi_kill_bonus": 100
    }
  },
  
  "combat_bonuses": {
    "bot_kill": 15,
    "player_kill": 25,
    "vehicle_kill": 50,
    "vehicle_assisted_kill": 35,
    "building_destruction": 10
  }
}
```

## 🎯 Estrategias de Juego

### Con Bots
- **Práctica segura**: Jugar contra bots en modo casual
- **Farming EVT**: Bots dropean tokens garantizados
- **Warm-up**: Calibrar puntería antes de ranked

### Con Vehículos
- **Tanque**: Lento pero resistente, ideal para equipos
- **Auto**: Rotaciones rápidas entre zonas
- **Dron**: Reconocimiento aéreo y ataque sorpresa
- **Mech**: Dominio de zonas abiertas
- **Excavadora**: Destruir cover enemigo

### Combos Efectivos
1. **Squad + Auto Blindado**: 4 jugadores moviéndose juntos
2. **Mech + Soporte**: 1 piloto + 3 jugadores protegiendo
3. **Dron + Francotirador**: Spotting desde aire + kills terrestres
4. **Tanque + Excavadora**: Destrucción total de área

## 🔧 Implementación Técnica

### Requisitos Unity
```
- Unity NavMesh Components
- Photon PUN 2 (multiplayer)
- Physics Layers:
  * Player (8)
  * Bot (9)
  * Vehicle (10)
  * Projectile (11)
```

### Scripts Necesarios
1. `BotManager.cs` - Spawn y gestión de bots
2. `BattleBot.cs` - IA individual de bot
3. `VehicleManager.cs` - Spawn de vehículos
4. `VehicleController.cs` - Control de vehículos
5. `PowerUp.cs` - Health packs y munición (nuevo)

### Dependencias
- Unity NavMesh: Para pathfinding de bots
- Photon Transform View: Sincronización de movimiento
- Rigidbody: Física de vehículos

## 🚀 Próximos Pasos

1. **Crear Prefabs 3D**
   - Modelos de bots (humanoid, terminator, drone)
   - Modelos de vehículos (5 tipos)
   - Animaciones de disparo y movimiento

2. **Sistema de Munición**
   - Pickups de ammo en mapa
   - Recarga automática en vehículos
   - Ammo drops de bots eliminados

3. **Efectos Visuales**
   - Partículas de disparo
   - Explosiones de vehículos
   - Trails de proyectiles

4. **Audio**
   - Sonidos de motores
   - Disparos de armas pesadas
   - Explosiones

5. **Balanceo**
   - Testear y ajustar stats de bots
   - Balancear daño de vehículos
   - Ajustar recompensas EVT

## 📈 Métricas de Éxito

### KPIs del Sistema
- Ratio de victorias Bot vs Player: 40/60 ideal
- Tiempo promedio de vida de vehículos: 3-5 minutos
- Tokens ganados por hora: 200-500 EVT
- Satisfacción de jugadores con IA: >4/5 estrellas

### Telemetría
```python
# Tracking en combat_arena.py
analytics = {
    "bot_kills": 0,
    "player_kills": 0,
    "vehicle_kills": 0,
    "vehicles_destroyed": 0,
    "avg_vehicle_lifetime": 0,
    "bot_accuracy": 0,
    "evt_earned_from_bots": 0
}
```
