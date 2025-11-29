# Guía de Implementación: Battle Arena Play-to-Earn
# Arenas de combate estilo Population One para Meta Horizon y Spatial.io

## 📋 Resumen del Sistema

Sistema completo de batalla royale VR con integración blockchain para:
- **Meta Horizon Worlds** (Meta Quest 3)
- **Spatial.io** (multiplataforma)

### Características Principales
- Battle Royale con hasta 100 jugadores
- Recompensas en criptomonedas (MVT tokens)
- NFTs coleccionables por victorias
- Sistema de armas con skins NFT
- Power-ups y equipamiento
- Torneos con premios

---

## 🗂️ Estructura de Archivos

```
mundo virtual/
├── battle-arena-system/
│   ├── combat_arena.py          # Backend: Lógica de combate
│   ├── play_to_earn.py          # Backend: Sistema de recompensas
│   └── arena_config.json        # Configuración de arenas
│
├── unity-metaverse/Assets/Scripts/BattleArena/
│   ├── BattleArenaManager.cs    # Unity: Gestor principal
│   ├── BattlePlayer.cs          # Unity: Controlador de jugador
│   └── WeaponController.cs      # Unity: Sistema de armas
│
└── spatial-scripts/
    └── battle-arena.ts          # Spatial.io: Sistema TypeScript
```

---

## 🚀 Paso 1: Configurar Unity para Meta Horizon

### 1.1 Instalar Dependencias

```bash
# Instalar Unity 2021.3 LTS
# Instalar Meta XR SDK desde Package Manager
# Instalar Photon PUN 2 para multiplayer
# Instalar Web3Unity para blockchain
```

### 1.2 Configurar Proyecto Unity

1. Crear proyecto Unity 3D
2. Importar Meta XR All-in-One SDK
3. Configurar Build Settings para Android (Meta Quest)
4. Añadir Photon App ID en `Photon Server Settings`

### 1.3 Configurar Scripts

1. Copiar scripts de `unity-metaverse/Assets/Scripts/BattleArena/` a tu proyecto
2. Crear prefabs:
   - `BattlePlayer.prefab` con componentes:
     - `BattlePlayer.cs`
     - `CharacterController`
     - `PhotonView`
     - `Animator`
   
3. Configurar Scene:
   - Añadir `BattleArenaManager` a objeto vacío
   - Crear spawn points (100+ transforms distribuidos)
   - Añadir safe zone visual (esfera con shader semi-transparente)

### 1.4 Configurar VR

```csharp
// En BattleArenaManager.cs, asegurar VR setup:
- XR Origin con Camera Offset
- Left/Right Hand Controllers
- Locomotion System (Continuous Move)
- Climbing/Flying mechanics
```

---

## 🎮 Paso 2: Crear Arenas en Meta Horizon Worlds

### 2.1 Exportar Assets de Unity

1. Seleccionar modelos 3D de arena
2. Exportar como glTF 2.0:
   ```
   File > Export > glTF 2.0
   ```
3. Optimizar con Draco compression

### 2.2 Importar a Meta Horizon

1. Abrir Meta Horizon Worlds Creator
2. Crear nuevo mundo "Battle Arena"
3. Importar assets glTF
4. Configurar:
   - Max Capacity: 100 jugadores
   - Physics: Enabled
   - Script Size Limit: 500KB

### 2.3 Configurar Scripting

Meta Horizon usa visual scripting (bloques), pero para lógica compleja:

1. Usar script blocks para:
   - Detectar entrada de jugadores
   - Trigger eventos de zona segura
   - Registrar eliminaciones

2. Conectar con backend Python vía HTTP:
   ```
   On Player Joined -> HTTP POST -> api/player/join
   On Player Eliminated -> HTTP POST -> api/player/eliminated
   ```

---

## 🌐 Paso 3: Configurar Spatial.io

### 3.1 Preparar Assets

1. Exportar modelos Unity como GLB:
   ```bash
   Unity > Assets > Export Package
   Convertir a GLB usando glTF Tools
   ```

2. Subir a Spatial:
   - Ir a studio.spatial.io
   - Crear nuevo Space
   - Upload GLB assets

### 3.2 Configurar TypeScript Script

1. Copiar `spatial-scripts/battle-arena.ts` a tu proyecto Spatial
2. Instalar Spatial SDK:
   ```bash
   npm install @spatial/spatial-scripting
   ```

3. Compilar TypeScript:
   ```bash
   npm run build
   ```

4. Subir bundle a Spatial Studio

### 3.3 Configurar Multiplayer

En Spatial Studio:
1. Enable Multiplayer (hasta 50 jugadores)
2. Configure Voice Chat (proximity-based)
3. Set Network Tick Rate: 60 Hz

---

## 💰 Paso 4: Integración Blockchain

### 4.1 Desplegar Smart Contracts

#### Contrato ERC20 (MVT Token)

```solidity
// contracts/MVTToken.sol
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MVTToken is ERC20 {
    constructor() ERC20("MetaversoToken", "MVT") {
        _mint(msg.sender, 1000000000 * 10 ** 18);
    }
}
```

#### Contrato ERC721 (Battle NFTs)

```solidity
// contracts/BattleNFT.sol
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract BattleNFT is ERC721 {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    
    mapping(uint256 => BattleMetadata) public nftMetadata;
    
    struct BattleMetadata {
        string playerName;
        uint256 kills;
        uint256 matchId;
        string rarity;
    }
    
    constructor() ERC721("BattleArena NFT", "BNFT") {}
    
    function mintVictoryNFT(
        address winner,
        string memory playerName,
        uint256 kills,
        uint256 matchId,
        string memory rarity
    ) public returns (uint256) {
        _tokenIds.increment();
        uint256 newNftId = _tokenIds.current();
        
        _mint(winner, newNftId);
        
        nftMetadata[newNftId] = BattleMetadata(
            playerName,
            kills,
            matchId,
            rarity
        );
        
        return newNftId;
    }
}
```

### 4.2 Desplegar a Polygon

```bash
# Instalar Hardhat
npm install --save-dev hardhat

# Configurar hardhat.config.js
module.exports = {
  solidity: "0.8.0",
  networks: {
    polygon: {
      url: "https://polygon-rpc.com/",
      accounts: [PRIVATE_KEY]
    }
  }
};

# Desplegar
npx hardhat run scripts/deploy.js --network polygon
```

### 4.3 Configurar Backend Python

Actualizar `battle-arena-system/play_to_earn.py`:

```python
from web3 import Web3

# Conectar a Polygon
w3 = Web3(Web3.HTTPProvider('https://polygon-rpc.com/'))

# Direcciones de contratos desplegados
TOKEN_CONTRACT = '0x...'  # Dirección MVT
NFT_CONTRACT = '0x...'    # Dirección BattleNFT

# ABI de contratos
TOKEN_ABI = [...]
NFT_ABI = [...]

# Crear instancias
token_contract = w3.eth.contract(address=TOKEN_CONTRACT, abi=TOKEN_ABI)
nft_contract = w3.eth.contract(address=NFT_CONTRACT, abi=NFT_ABI)
```

---

## 🔧 Paso 5: Configurar Backend API

### 5.1 Extender Flask Server

Añadir a `metaverso_professional.py`:

```python
from battle_arena_system.combat_arena import CombatArenaSystem
from battle_arena_system.play_to_earn import PlayToEarnSystem

# Inicializar sistemas
arena_system = CombatArenaSystem()
p2e_system = PlayToEarnSystem()

@app.route('/api/arena/join', methods=['POST'])
def join_arena():
    data = request.json
    player_id = data['player_id']
    wallet = data['wallet_address']
    
    arena_id = arena_system.join_random_arena(player_id, wallet)
    return jsonify({'arena_id': arena_id})

@app.route('/api/arena/eliminate', methods=['POST'])
def player_eliminated():
    data = request.json
    victim_id = data['victim_id']
    killer_id = data['killer_id']
    
    # Procesar eliminación
    arena_system.eliminate_player(victim_id, killer_id)
    
    # Otorgar recompensa por kill
    reward = p2e_system.calculate_kill_reward()
    p2e_system.send_token_reward(killer_id, reward)
    
    return jsonify({'success': True})

@app.route('/api/arena/victory', methods=['POST'])
def declare_victory():
    data = request.json
    winner_id = data['winner_id']
    stats = data['stats']
    
    # Calcular recompensa total
    reward = p2e_system.calculate_match_reward(
        placement=1,
        kills=stats['kills'],
        damage=stats['damage'],
        survival_time=stats['survival_time']
    )
    
    # Enviar tokens
    tx_hash = p2e_system.send_token_reward(winner_id, reward)
    
    # Mintear NFT si tiene suerte
    nft_id = p2e_system.try_mint_nft(winner_id, stats)
    
    return jsonify({
        'reward': reward,
        'tx_hash': tx_hash,
        'nft_id': nft_id
    })
```

### 5.2 Configurar WebSocket para Real-Time

```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('player_position')
def handle_position(data):
    # Broadcast posición a otros jugadores
    emit('position_update', data, broadcast=True, include_self=False)

@socketio.on('zone_shrink')
def handle_zone_shrink(data):
    # Notificar nueva zona
    emit('safe_zone_update', data, broadcast=True)
```

---

## 🎯 Paso 6: Testing

### 6.1 Test Local (Unity)

1. Abrir Unity Scene
2. Configurar Photon PUN:
   - Usar región local
   - Max 10 jugadores para test
3. Build and Run en Meta Quest (ADB)
4. Probar con 2-4 jugadores

### 6.2 Test Backend

```bash
# Iniciar servidor Flask
python metaverso_professional.py

# Test endpoints
curl -X POST http://localhost:5000/api/arena/join \
  -H "Content-Type: application/json" \
  -d '{"player_id": "123", "wallet_address": "0x..."}'
```

### 6.3 Test Blockchain (Testnet)

1. Desplegar contratos en Polygon Mumbai (testnet)
2. Obtener tokens MATIC de faucet
3. Probar transacciones de prueba
4. Verificar en PolygonScan

---

## 📊 Paso 7: Configurar Analytics

### 7.1 Dashboard de Métricas

Crear en `templates/arena_dashboard.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Battle Arena Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>📊 Battle Arena Analytics</h1>
    
    <div id="active-players-chart"></div>
    <div id="rewards-distribution-chart"></div>
    <div id="nft-minted-chart"></div>
    
    <script>
        // Fetch data y crear gráficos
        fetch('/api/analytics/players')
            .then(res => res.json())
            .then(data => {
                Plotly.newPlot('active-players-chart', [{
                    x: data.timestamps,
                    y: data.player_counts,
                    type: 'scatter'
                }]);
            });
    </script>
</body>
</html>
```

---

## 🚢 Paso 8: Deployment a Producción

### 8.1 Deploy Smart Contracts a Mainnet

```bash
# Polygon Mainnet
npx hardhat run scripts/deploy.js --network polygon

# Guardar direcciones
# TOKEN_CONTRACT: 0x...
# NFT_CONTRACT: 0x...
```

### 8.2 Deploy Backend a Cloud

```bash
# Opción 1: AWS EC2
# Opción 2: Google Cloud Run
# Opción 3: Heroku

# Dockerfile
FROM python:3.13
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "metaverso_professional.py"]
```

### 8.3 Publicar en Meta Horizon

1. Finalizar mundo en Horizon Worlds Creator
2. Submit para revisión
3. Esperar aprobación (1-2 semanas)
4. Publicar a audiencia pública

### 8.4 Publicar en Spatial.io

1. Finalizar Space en Spatial Studio
2. Configurar permisos (público/privado)
3. Publish Space
4. Compartir URL

---

## 💡 Configuración de Economía

### Recompensas Sugeridas

```python
# En arena_config.json (ya configurado)
{
  "rewards": {
    "victory": 1000,      # MVT por ganar
    "kill": 25,           # MVT por eliminación
    "top_10": 250,        # MVT por top 10
    "participation": 50,  # MVT por jugar
    "headshot": 10,       # Bonus headshot
    "nft_drop_rate": 0.15 # 15% probabilidad NFT
  }
}
```

### Costos de Entrada

- **Partidas Casuales**: Gratis
- **Partidas Ranked**: 10 MVT
- **Torneos Diarios**: 50 MVT
- **Torneos Semanales**: 100 MVT

---

## 🔒 Seguridad

### Anti-Cheat

1. **Server-Side Validation**: Todas las acciones validadas en servidor
2. **Photon Anti-Cheat**: Activar en Photon Dashboard
3. **Rate Limiting**: Limitar API calls

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/arena/eliminate')
@limiter.limit("10 per minute")
def eliminate():
    pass
```

---

## 📱 Soporte Multi-Plataforma

### VR Headsets Soportados
- ✅ Meta Quest 3
- ✅ Meta Quest 2
- ✅ Valve Index
- ✅ HTC Vive
- ✅ PSVR 2 (futuro)

### Desktop/Mobile
- 🖥️ PC (Steam)
- 📱 iOS (futuro)
- 📱 Android (futuro)

---

## 🎉 Siguientes Pasos

1. ✅ Crear mapas 3D detallados
2. ✅ Implementar sistema de clanes
3. ✅ Añadir modos de juego adicionales
4. ✅ Marketplace de NFTs
5. ✅ Sistema de apuestas
6. ✅ Streaming integration (Twitch)

---

## 📞 Recursos

- [Meta XR SDK Docs](https://developer.oculus.com/documentation/)
- [Spatial.io Docs](https://docs.spatial.io/)
- [Photon PUN 2](https://doc.photonengine.com/pun/v2/)
- [Web3Unity](https://github.com/ChainSafe/web3.unity)
- [OpenZeppelin Contracts](https://docs.openzeppelin.com/contracts/)

---

**¡Sistema listo para lanzamiento!** 🚀
