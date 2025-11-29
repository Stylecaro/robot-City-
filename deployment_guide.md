# Guía de Deployment - Metaverso Professional

## 📋 Preparación para Blockchain

### 1. Configuración de Smart Contracts

#### Ethereum/Polygon/BSC
```bash
# Instalar dependencias
npm install --save-dev hardhat @openzeppelin/contracts ethers

# Inicializar proyecto Hardhat
npx hardhat init

# Compilar contratos
npx hardhat compile

# Desplegar a testnet
npx hardhat run scripts/deploy.js --network sepolia
```

#### Contratos a Desplegar
- **LandOwnership.sol** - ERC721 para parcelas virtuales
- **MetaversoToken.sol** - ERC20 para economía virtual
- **Marketplace.sol** - ERC1155 para comercio

### 2. Almacenamiento IPFS

```bash
# Subir assets a IPFS
npm install -g @pinata/sdk

# Script de subida
node scripts/upload_to_ipfs.js
```

## 🌐 Deployment a Meta Horizon Worlds

### Requisitos
- Meta Quest 2/3/Pro
- Cuenta de Meta Developer
- Unity 2021.3+ con Horizon SDK

### Pasos de Exportación

1. **Preparar Assets 3D**
```bash
# Optimizar modelos 3D
- Máximo 500k polígonos totales
- Texturas 2048x2048 máximo
- Formato glTF 2.0 con compresión Draco
```

2. **Configurar en Unity**
```csharp
// Importar Horizon SDK
using Meta.Horizon;

// Configurar world settings
WorldSettings.MaxCapacity = 50;
WorldSettings.PhysicsEnabled = true;
```

3. **Build y Upload**
```bash
# Build para Meta Horizon
Unity > File > Build Settings > Meta Horizon Platform
Unity > Meta > Upload to Horizon Worlds
```

## 🎮 Deployment a Spatial.io

### Requisitos
- Cuenta Spatial Creator
- Assets en formato GLB
- TypeScript para scripting

### Pasos de Deployment

1. **Preparar Espacio**
```bash
# Instalar Spatial CLI
npm install -g @spatial/cli

# Inicializar proyecto
spatial init metaverso-professional
```

2. **Configurar Assets**
```typescript
// spatial.config.ts
export default {
  name: "Metaverso Professional",
  maxVisitors: 50,
  environment: "custom",
  assets: {
    buildings: "./assets/buildings/",
    robots: "./assets/robots/",
    vehicles: "./assets/vehicles/"
  }
}
```

3. **Deploy**
```bash
# Test local
spatial dev

# Deploy a producción
spatial deploy --production
```

## 🔐 Configuración de Seguridad

### Variables de Entorno
```env
# .env
BLOCKCHAIN_PRIVATE_KEY=your_private_key
INFURA_PROJECT_ID=your_infura_id
PINATA_API_KEY=your_pinata_key
PINATA_SECRET_KEY=your_pinata_secret
META_APP_ID=your_meta_app_id
SPATIAL_API_KEY=your_spatial_key
```

### Encriptación
```python
# Encriptar configuraciones sensibles
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)
encrypted_config = cipher.encrypt(config_data)
```

## 📊 Métricas y Monitoreo

### Analytics
```javascript
// Integrar analytics
import { Analytics } from '@spatial/analytics';

Analytics.track('user_entered_city');
Analytics.track('robot_interaction', { robot_id: 'R001' });
```

### Performance Monitoring
```python
# Server monitoring
import prometheus_client
from prometheus_client import Counter, Histogram

request_count = Counter('metaverso_requests', 'Total requests')
response_time = Histogram('metaverso_response_time', 'Response time')
```

## 🚀 Lista de Verificación Pre-Deployment

### Blockchain
- [ ] Contratos auditados
- [ ] Gas optimization completado
- [ ] Testnet deployment exitoso
- [ ] Metadata en IPFS
- [ ] Frontend integrado con Web3

### Meta Horizon
- [ ] Assets optimizados (<100MB)
- [ ] Physics configurado
- [ ] Multiplayer testeado
- [ ] Voice chat funcionando
- [ ] Performance 90fps+

### Spatial.io
- [ ] GLB models optimizados
- [ ] Scripts TypeScript validados
- [ ] Interacciones testeadas
- [ ] Mobile compatible
- [ ] VR tested

## 📦 Scripts de Automatización

### Deploy Todo
```bash
#!/bin/bash
# deploy_all.sh

echo "Deploying to Blockchain..."
npm run deploy:blockchain

echo "Uploading to IPFS..."
npm run upload:ipfs

echo "Building for Meta Horizon..."
npm run build:horizon

echo "Deploying to Spatial..."
npm run deploy:spatial

echo "✅ Deployment completo!"
```

## 🔄 Actualización Continua

### CI/CD Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy Metaverso

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Blockchain
        run: npm run deploy:blockchain
      - name: Deploy to Spatial
        run: npm run deploy:spatial
```

## 📞 Soporte

- **Blockchain**: docs.ethereum.org
- **Meta Horizon**: developers.meta.com/horizon
- **Spatial**: docs.spatial.io

---

**Sistema preparado para deployment multi-plataforma** ✅
