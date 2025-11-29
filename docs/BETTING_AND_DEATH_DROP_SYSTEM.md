# 🎮 Sistema de Apuestas y Death Drop - Battle Arena

## 📋 Resumen

Sistema completo implementado con las siguientes características:

### 1. **Sistema de Apuestas** (BettingSystem.cs)
- Jugadores deben pagar entrada para participar
- El pool de apuestas se distribuye:
  - 70% para premios
  - 25% para gastos operativos
  - 5% comisión de plataforma
- Diferentes costos según tipo de partida:
  - Casual: GRATIS
  - Ranked: 10 MVT
  - Torneo: 50 MVT
  - High Stakes: 100 MVT

### 2. **Sistema Death Drop** (DeathDropSystem.cs)
- Cuando mueres, pierdes el 100% de las criptomonedas que portabas
- Se crea una "loot box" en el lugar de muerte
- Otros jugadores pueden recoger el botín
- El killer obtiene los tokens automáticamente
- También se dropean:
  - Armas equipadas
  - Items del inventario
  - Munición

### 3. **Mapas 3D** (MapGenerator.cs)
4 tipos de mapas:

#### a) Battle Arena
- Combate PvP intenso
- 150 edificios
- 500 árboles/rocas
- 50 spawn de armas
- 30 power-ups
- 100 spawn points para jugadores

#### b) Open World
- Mapa de 10km x 10km
- 5 ciudades
- 10 bosques
- 20 estaciones de aprendizaje
- 50 NPCs con misiones
- Exploración libre

#### c) Learning Zone
- Zona educativa
- 15 salas de aprendizaje
- 10 zonas de práctica
- 25 tutoriales interactivos
- Arena de práctica
- Ideal para principiantes

#### d) Tournament
- Mapa balanceado para competición
- Terreno simétrico
- Edificios equidistantes
- Armas balanceadas
- 100 spawn points equitativos

### 4. **Wallet System** (CryptoWalletSystem.cs)
- Conexión con MetaMask
- Verificación de balance
- Deducción de tokens (entrada)
- Envío de tokens (premios)
- Minteo de NFTs
- Compatible con Web3Unity

---

## 🎯 Flujo del Juego

### 1. Antes de la Partida
```
Jugador se conecta → Verifica wallet → Paga entrada → Se une a partida
```

### 2. Durante la Partida
```
Jugador porta tokens → Mata enemigos → Recoge botín → Acumula más tokens
```

### 3. Al Morir
```
Jugador muere → Pierde tokens portados → Crea loot box → Otros recogen
```

### 4. Al Ganar
```
Victoria → Prize pool se distribuye → Top 8 reciben premios → NFT aleatorio
```

---

## 💰 Economía del Juego

### Costos de Entrada
| Tipo | Entrada | Pool | Ganancia Top 1 |
|------|---------|------|----------------|
| Casual | 0 MVT | 0 MVT | Kills only |
| Ranked | 10 MVT | 700 MVT | 280 MVT (40%) |
| Torneo | 50 MVT | 3,500 MVT | 1,400 MVT (40%) |
| High Stakes | 100 MVT | 7,000 MVT | 2,800 MVT (40%) |

*Asumiendo 100 jugadores*

### Distribución de Premios
1. **1er lugar**: 40% del pool
2. **2do lugar**: 25% del pool
3. **3er lugar**: 15% del pool
4. **4to lugar**: 8% del pool
5. **5to lugar**: 5% del pool
6. **6to lugar**: 3% del pool
7. **7mo lugar**: 2% del pool
8. **8vo lugar**: 2% del pool

### Sistema Death Drop
- **100% loss**: Pierdes TODO lo que portas
- **Loot box**: Dura 5 minutos antes de desaparecer
- **Transfer**: Killer recibe tokens automáticamente
- **Seguro opcional**: Proteger tokens (próximamente)

---

## 🗺️ Tipos de Mapas

### 1. Battle Arena (PvP)
```
Tamaño: 5km x 5km
Jugadores: 100
Edificios: 150
Armas: 50 spawns
Power-ups: 30
Vegetación: 500+
```

### 2. Open World (Exploración)
```
Tamaño: 10km x 10km
Jugadores: 20
Ciudades: 5
NPCs: 50
Misiones: Ilimitadas
Aprendizaje: 20 estaciones
```

### 3. Learning Zone (Educativo)
```
Tamaño: 2km x 2km
Jugadores: 1-10
Salas: 15
Tutoriales: 25
Arena práctica: 1
Dificultad: Fácil
```

### 4. Tournament (Competitivo)
```
Tamaño: 5km x 5km
Jugadores: 100
Simetría: Total
Balance: Perfecto
Spawn: Equitativo
```

---

## 🔧 Integración

### En Unity
1. Añadir `MapGenerator` a escena
2. Configurar tipo de mapa
3. Asignar prefabs (edificios, armas, etc)
4. Ejecutar `GenerateMap()`

### En BattleArenaManager
```csharp
// Ya integrado automáticamente
bettingSystem // Cobra entradas
deathDropSystem // Maneja drops al morir
```

### En BattlePlayer
```csharp
// Nuevas variables
player.entryFeePaid // Entrada pagada
player.carriedTokens // Tokens portados (se pierden al morir)
player.hasInsurance // Seguro opcional
```

---

## 🎮 Mecánicas de Juego

### Ganar Tokens
- ✅ Matar enemigos (+25 MVT)
- ✅ Recoger loot boxes
- ✅ Ganar partida (40% pool)
- ✅ Top 10 (distribución proporcional)

### Perder Tokens
- ❌ Morir (pierdes todo lo portado)
- ❌ Pagar entrada (antes de jugar)

### Protección
- 🛡️ Seguro opcional (próximamente)
- 🛡️ Guardar tokens en wallet antes de morir
- 🛡️ Jugar en modo casual (sin apuestas)

---

## 📊 Estadísticas de Ejemplo

### Partida de 100 jugadores (Torneo 50 MVT)
```
Total recaudado: 5,000 MVT
Prize pool (70%): 3,500 MVT
Gastos (25%): 1,250 MVT
Comisión (5%): 250 MVT

Premios:
1º: 1,400 MVT (28x entrada)
2º: 875 MVT (17.5x entrada)
3º: 525 MVT (10.5x entrada)
4º: 280 MVT (5.6x entrada)
5º: 175 MVT (3.5x entrada)
...
```

### Jugador Promedio
```
Partidas jugadas: 10
Entrada promedio: 50 MVT
Total invertido: 500 MVT

Victorias: 1
Top 3: 2
Kills totales: 45
Botín recogido: 300 MVT

Total ganado: 2,200 MVT
Ganancia neta: +1,700 MVT (340%)
```

---

## 🚀 Próximos Pasos

1. **Crear prefabs 3D**:
   - Edificios variados
   - Árboles y vegetación
   - Armas y power-ups
   - Loot box visual

2. **Sistema de seguros**:
   - Comprar seguro antes de partida
   - Proteger % de tokens al morir
   - Costo basado en cantidad asegurada

3. **Ranking global**:
   - Leaderboards por ganancias
   - Leaderboards por kills
   - Temporadas con premios especiales

4. **Eventos especiales**:
   - Torneos con mega premios
   - Double rewards days
   - NFT drop rate boost

---

**Sistema completo y listo para integrar** ✅
