# NEURONAR API

Documentacion operativa del sistema AI NEURONAR para Ciudad Robot.

## Base URL

```bash
http://localhost:8010/api/ai/neuronar
```

## Resumen

NEURONAR incorpora:

- Nucleo cuantico de Ciudad Robot
- Cadena de bloques cuantica
- Capa Web3 para identidades y anclaje de activos

## Endpoints

### Estado y control

- `GET /api/ai/neuronar`
- `POST /api/ai/neuronar/boot`
- `POST /api/ai/neuronar/inference`

### Nucleo cuantico

- `GET /api/ai/neuronar/quantum-core`
- `POST /api/ai/neuronar/quantum-core/calibrate`

### Cadena cuantica

- `GET /api/ai/neuronar/quantum-chain`
- `POST /api/ai/neuronar/quantum-chain/transactions`
- `POST /api/ai/neuronar/quantum-chain/blocks`
- `GET /api/ai/neuronar/quantum-chain/verify`

### Web3

- `GET /api/ai/neuronar/web3/identities`
- `POST /api/ai/neuronar/web3/identities`
- `POST /api/ai/neuronar/web3/anchor`

### Documentacion API

- `GET /api/ai/neuronar/docs`

## Ejemplos curl

### 1) Estado general

```bash
curl -X GET http://localhost:8010/api/ai/neuronar
```

### 2) Boot del sistema

```bash
curl -X POST http://localhost:8010/api/ai/neuronar/boot \
  -H 'Content-Type: application/json' \
  -d '{"mode":"standard"}'
```

### 3) Calibrar nucleo cuantico

```bash
curl -X POST http://localhost:8010/api/ai/neuronar/quantum-core/calibrate \
  -H 'Content-Type: application/json' \
  -d '{"profile":"precision"}'
```

### 4) Inferencia NEURONAR

```bash
curl -X POST http://localhost:8010/api/ai/neuronar/inference \
  -H 'Content-Type: application/json' \
  -d '{"task_type":"resource-allocation","input":{"zone":"north","load":0.72}}'
```

### 5) Crear transaccion cuantica

```bash
curl -X POST http://localhost:8010/api/ai/neuronar/quantum-chain/transactions \
  -H 'Content-Type: application/json' \
  -d '{"from":"core-robot-1","to":"core-robot-7","payload":{"task":"energy-balance"},"energy_cost":0.44}'
```

### 6) Minar bloque cuantico

```bash
curl -X POST http://localhost:8010/api/ai/neuronar/quantum-chain/blocks \
  -H 'Content-Type: application/json' \
  -d '{"validator":"city-validator-a"}'
```

### 7) Verificar integridad de cadena

```bash
curl -X GET http://localhost:8010/api/ai/neuronar/quantum-chain/verify
```

### 8) Registrar identidad Web3

```bash
curl -X POST http://localhost:8010/api/ai/neuronar/web3/identities \
  -H 'Content-Type: application/json' \
  -d '{"alias":"city-wallet"}'
```

### 9) Anclar activo Web3

```bash
curl -X POST http://localhost:8010/api/ai/neuronar/web3/anchor \
  -H 'Content-Type: application/json' \
  -d '{"asset_id":"robot-nft-001","metadata":{"tier":"legendary","origin":"ciudad-robot"}}'
```

## Payloads de referencia

### POST /boot

```json
{
  "mode": "standard"
}
```

Modos permitidos:

- `standard`
- `safe`
- `high-performance`

### POST /quantum-core/calibrate

```json
{
  "profile": "balanced"
}
```

Perfiles permitidos:

- `balanced`
- `precision`
- `throughput`

### POST /inference

```json
{
  "task_type": "diagnostic",
  "input": {
    "node": "sector-7",
    "signals": [0.12, 0.44, 0.98]
  }
}
```

`task_type` permitidos:

- `diagnostic`
- `routing`
- `threat-assessment`
- `resource-allocation`

### POST /quantum-chain/transactions

```json
{
  "from": "core-robot-1",
  "to": "core-robot-7",
  "payload": {
    "task": "energy-balance"
  },
  "energy_cost": 0.44
}
```

### POST /web3/identities

```json
{
  "alias": "tesla-bot-wallet"
}
```

### POST /web3/anchor

```json
{
  "asset_id": "robot-nft-001",
  "metadata": {
    "tier": "legendary",
    "origin": "ciudad-robot"
  }
}
```

## Notas

- La implementacion actual es en memoria para prototipado rapido.
- La cadena cuantica incluye bloque genesis y verificacion de integridad por hash.
- La capa Web3 permite registrar identidades y anclar activos en la cadena cuantica.
