# Web3 — Multi-Chain Integration Layer

Provides blockchain adapters for Robot City's on-chain features.  
All adapters use only the **Python standard library** for address validation.  
Live on-chain operations require the chain-specific library noted below.

---

## Supported Chains

| Chain | Adapter Class | Required Library | Address Format |
|---|---|---|---|
| Ethereum | `EVMAdapter` | `web3` (pip) | `0x` + 40 hex |
| Polygon | `EVMAdapter` | `web3` | `0x` + 40 hex |
| BNB Smart Chain | `EVMAdapter` | `web3` | `0x` + 40 hex |
| Arbitrum | `EVMAdapter` | `web3` | `0x` + 40 hex |
| Optimism | `EVMAdapter` | `web3` | `0x` + 40 hex |
| Base | `EVMAdapter` | `web3` | `0x` + 40 hex |
| Avalanche C-Chain | `EVMAdapter` | `web3` | `0x` + 40 hex |
| Solana | `SolanaAdapter` | `solana` (pip) | Base58, 32–44 chars |
| Bitcoin | `BitcoinAdapter` | Esplora REST API | 1…, 3…, bc1… |
| Lightning | `LightningAdapter` | LND/CLN node | BOLT-11 |
| Tron | `TronAdapter` | `tronpy` (pip) | T + 33 base58 |

---

## Quick Start

```python
from web3 import ChainRegistry, ChainType

# Create a registry with all default adapters
registry = ChainRegistry.get_default_registry()

# Validate addresses (works offline, stdlib only)
eth_adapter = registry.get_adapter(ChainType.ETHEREUM)
print(eth_adapter.validate_address("0xAb5801a7D398351b8bE11C439e05C5b3259aec9B"))  # True

sol_adapter = registry.get_adapter(ChainType.SOLANA)
print(sol_adapter.validate_address("So11111111111111111111111111111111111111112"))  # True

btc_adapter = registry.get_adapter(ChainType.BITCOIN)
print(btc_adapter.validate_address("bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq"))  # True

# Registry-level validation
valid = registry.validate_address_on_chain(ChainType.TRON, "TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW")
print(valid)  # True
```

---

## Live On-Chain Usage (requires library)

```python
# After: pip install web3
from web3 import EVMAdapter, ChainType

eth = EVMAdapter.create_ethereum(rpc_url="https://mainnet.infura.io/v3/YOUR_KEY")
balance = eth.get_balance("0xYourAddress", "ETH")
```

---

## Adding a New Chain Adapter

1. Add a member to `ChainType` in `base_chain.py`.
2. Create `my_chain_adapter.py` implementing `ChainAdapter`:

```python
from .base_chain import ChainAdapter, ChainType, NetworkConfig, TransactionRecord

class MyChainAdapter(ChainAdapter):
    def validate_address(self, address: str) -> bool:
        # stdlib-only validation
        ...

    def get_balance(self, address: str, token: str = "") -> float:
        # TODO: requires my-chain-sdk
        raise RuntimeError("Install my-chain-sdk")

    def send_transaction(self, from_addr, to_addr, amount, token, private_key):
        raise RuntimeError("Install my-chain-sdk")

    def get_transaction(self, tx_hash: str) -> TransactionRecord:
        raise RuntimeError("Install my-chain-sdk")

    def get_network_config(self) -> NetworkConfig:
        return NetworkConfig(
            chain_type=ChainType.MY_CHAIN,
            network_name="My Chain Mainnet",
            native_token="MYT",
            explorer_url="https://myexplorer.io",
        )
```

3. Register in `ChainRegistry.get_default_registry()`.
4. Export from `__init__.py`.

---

## Important Notes on RPC URLs

> **You must supply your own RPC URL for every on-chain operation.**

Never hardcode API keys.  Use environment variables:

```python
import os
rpc = os.environ["ETH_RPC_URL"]
adapter = EVMAdapter.create_ethereum(rpc_url=rpc)
```

---

## Module Structure

```
web3/
├── __init__.py          # Public API
├── base_chain.py        # ChainType, NetworkConfig, TransactionRecord, ChainAdapter
├── evm_adapter.py       # EVMAdapter (Ethereum + all EVM chains)
├── solana_adapter.py    # SolanaAdapter
├── bitcoin_adapter.py   # BitcoinAdapter + LightningAdapter
├── tron_adapter.py      # TronAdapter
└── chain_registry.py    # ChainRegistry
```
