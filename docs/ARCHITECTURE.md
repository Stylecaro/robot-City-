# Robot City — Modular Architecture

This document describes the new modular foundation added to **robot-City-** for building a complete intelligent robot city platform with multi-chain blockchain support, crypto payments, post-quantum security, and city simulation.

---

## Directory structure

```
robot-City-/
│
├── service-robots/          # City service robot APIs
├── simulation-system/       # City simulation / game layer
├── web3/                    # Multi-chain blockchain adapters
├── payments/                # Crypto payment invoice workflow
├── wallets/                 # Wallet address validation & metadata
├── quantum-security/        # Post-quantum cryptography wrappers
├── quantum-blockchain/      # Hybrid quantum event/audit ledger
│
├── ai-engine/               # (existing) AI coordination engine
├── backend/                 # (existing) Node.js REST API
├── frontend/                # (existing) React + Three.js 3D UI
├── robot-system/            # (existing) Core robot AI
├── avatar-system/           # (existing) User avatars
├── blockchain/              # (existing) EVM smart contracts
└── battle-arena-system/     # (existing) Combat arena
```

---

## Module summaries

### `service-robots/`
City service robot APIs covering six domains:

| Class | Domain | Key capabilities |
|---|---|---|
| `MedicalRobot` | Medical | emergency response, diagnostics, medication delivery |
| `SecurityRobotService` | Security | patrol, threat detection, access control |
| `TransportRobot` | Transport | route planning, passenger/cargo delivery |
| `CommerceRobot` | Commerce | inventory, customer service, payments |
| `ConstructionRobot` | Construction | build, inspect, maintain structures |
| `EducationRobot` | Education | tutoring, assessments, interactive lessons |

All robots extend `ServiceRobot` and are managed by `ServiceRobotRegistry`.

**Quick start:**
```python
from service_robots import ServiceRobotRegistry, MedicalRobot, RobotType

registry = ServiceRobotRegistry()
bot = MedicalRobot(name="MediBot-1")
registry.register_robot(bot)

result = registry.dispatch_robot("medical", "respond_to_emergency")
```

---

### `simulation-system/`
Two-layer simulation system:

- `simulation_engine.py` — original combat/training simulation
- `city_simulation.py` — **new** city-level simulation with citizens, zones, incidents, and robot dispatch

**Quick start:**
```python
from simulation_system.city_simulation import CitySimulation

sim = CitySimulation(city_name="Ciudad Robot Alpha")
sim.initialize(num_citizens=50)

for _ in range(10):
    result = sim.tick()
    print(result["summary"])

state = sim.get_city_state()  # feed to frontend 3D viewer
```

---

### `web3/`
Multi-chain adapter layer. Supports:

| Chain | Adapter | Notes |
|---|---|---|
| Ethereum | `EVMAdapter` | EIP-55 address validation |
| Polygon | `EVMAdapter` | same adapter, different config |
| BNB Chain | `EVMAdapter` | — |
| Arbitrum | `EVMAdapter` | — |
| Optimism | `EVMAdapter` | — |
| Base | `EVMAdapter` | — |
| Avalanche | `EVMAdapter` | — |
| Solana | `SolanaAdapter` | base58 validation |
| Bitcoin | `BitcoinAdapter` | legacy / SegWit / Bech32 |
| Lightning | `LightningAdapter` | invoice create/pay placeholders |
| Tron | `TronAdapter` | T-address validation |

> **Note:** RPC calls (balance, send, etc.) are placeholder stubs. Wire up your own RPC URL and install `web3.py` / `solana-py` / `tronpy` as needed.

**Quick start:**
```python
from web3 import ChainRegistry

registry = ChainRegistry.get_default_registry()
adapter = registry.get_adapter("ETHEREUM")
print(adapter.validate_address("0xAbCd..."))
```

---

### `payments/`
Crypto invoice/payment workflow supporting:
`BTC`, `ETH`, `USDT`, `USDC`, `SOL`, `BNB`, `MATIC`, `TRX`

**Quick start:**
```python
from payments import CryptoPaymentService, SupportedAsset

svc = CryptoPaymentService()
invoice = svc.create_invoice(SupportedAsset.ETH, 0.05, "Robot rental fee")

instructions = svc.get_payment_instructions(invoice.invoice_id)
print(instructions["qr_code_data"])

receipt = svc.mark_paid(invoice.invoice_id, tx_hash="0x...", amount_received=0.05)
```

---

### `wallets/`
Safe wallet management — **no private key storage**.

```python
from wallets import WalletManager, WalletValidator

validator = WalletValidator()
print(validator.validate_address("0xAbCd...", "ETH"))

manager = WalletManager()
manager.add_wallet("user-001", "ETH", "0xAbCd...")
```

---

### `quantum-security/`
Post-quantum cryptography layer. Algorithms: `ML-DSA` (Dilithium), `ML-KEM`, `SPHINCS+`, `Falcon`.

> **Current status:** SHA3-256 hashing is real. Signing/encryption stubs require `liboqs-python` or `pqcrypto`.

```python
from quantum_security import PQCWrapper, KeyManager

km = KeyManager()
bundle = km.generate_key_bundle("robot-001")

pqc = PQCWrapper()
msg_hash = pqc.hash_message(b"hello city")
```

---

### `quantum-blockchain/`
Hybrid event/audit ledger. Three components:

| File | Purpose |
|---|---|
| `quantum_blockchain.py` | Quantum-signed local blockchain |
| `event_ledger.py` | **new** chain-agnostic event recording |
| `pqc_crypto.py` | ML-DSA (Dilithium) PQC implementation |

**Quick start:**
```python
from quantum_blockchain.event_ledger import EventLedger, EventCategory, QuantumBlockchainBackend

ledger = EventLedger()
ledger.add_backend(QuantumBlockchainBackend())

event = ledger.record_payment_event(
    invoice_id="inv-001",
    status="paid",
    details={"asset": "ETH", "amount": 0.05},
)
print(event.integrity_hash)
```

---

## Architecture diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Frontend (React + Three.js)            │
│                    Web UI / 3D City Viewer                │
└────────────────────────┬─────────────────────────────────┘
                         │ REST / WebSocket
┌────────────────────────▼─────────────────────────────────┐
│              Backend API (Node.js / FastAPI)              │
│         ai-engine │ backend │ simulation-system           │
└───┬────────┬──────┴────┬────────────┬────────────────────┘
    │        │           │            │
    ▼        ▼           ▼            ▼
service- payments/   web3/       quantum-
robots/             adapters    blockchain/
                               event_ledger
    │        │           │            │
    └────────┴───────────┴────────────┘
                wallets/   quantum-security/
```

---

## How to add a new chain

1. Create `web3/my_chain_adapter.py` extending `ChainAdapter`
2. Implement `validate_address`, `get_balance`, `send_transaction`, `get_transaction`, `get_network_config`
3. Add a `ChainType.MY_CHAIN` entry in `web3/base_chain.py`
4. Register in `ChainRegistry.get_default_registry()`

## How to add a new service robot

1. Create `service-robots/my_robot.py` extending `ServiceRobot`
2. Override `robot_type`, `capabilities`, and add domain-specific methods
3. Import and expose in `service-robots/__init__.py`

## How to record events on a real chain

1. Implement `ChainBackend` protocol from `quantum_blockchain/event_ledger.py`
2. Add your backend: `ledger.add_backend(MyEthereumBackend())`
3. All future `ledger.record(...)` calls will also send to that chain
