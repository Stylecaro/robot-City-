# Wallets — Safe Multi-Chain Wallet Management

> **Security-first design: private keys are never stored.**

This module manages *public addresses* only.  All signing must happen
in an external hardware wallet or secure enclave.

---

## Supported Chains

| Key | Chain | Address Format |
|---|---|---|
| `ETH` | Ethereum | `0x` + 40 hex |
| `BTC` | Bitcoin | Legacy / P2SH / Bech32 |
| `SOL` | Solana | Base58, 32–44 chars |
| `TRX` | Tron | `T` + 33 base58 |
| `BNB` | BNB Smart Chain | `0x` + 40 hex |
| `MATIC` | Polygon | `0x` + 40 hex |
| `AVAX` | Avalanche C-Chain | `0x` + 40 hex |
| `ARB` | Arbitrum | `0x` + 40 hex |
| `OP` | Optimism | `0x` + 40 hex |
| `BASE` | Base | `0x` + 40 hex |

---

## Quick Start

### Address Validation

```python
from wallets import WalletValidator

# Validate a single address
print(WalletValidator.validate_evm_address("0xAb5801a7D398351b8bE11C439e05C5b3259aec9B"))  # True
print(WalletValidator.validate_bitcoin_address("bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq"))  # True
print(WalletValidator.validate_solana_address("So11111111111111111111111111111111111111112"))  # True
print(WalletValidator.validate_tron_address("TJCnKsPa7y5okkXvQAidZBzqx3QyQ6sxMW"))  # True

# Chain-agnostic validation
result = WalletValidator.validate_address("0xAb580...", "ETH")
print(result)
# {"valid": True, "chain": "ETH", "address": "0xAb580...", "notes": "Valid EVM address."}
```

### Chain Metadata

```python
from wallets import WalletMetadata

info = WalletMetadata.get_chain_info("BTC")
print(info.chain_name)          # "Bitcoin"
print(info.address_format)      # "Legacy (1…), P2SH (3…), or Bech32 (bc1…)"
print(info.explorer_url_template)

url = WalletMetadata.get_explorer_url("ETH", "0xAb5801...")
print(url)  # "https://etherscan.io/address/0xAb5801..."

print(WalletMetadata.list_supported_chains())
```

### Wallet Manager

```python
from wallets import WalletManager

mgr = WalletManager()

# Register a wallet (validates address before storing)
mgr.add_wallet("alice_eth", "ETH", "0xAb5801a7D398351b8bE11C439e05C5b3259aec9B")
mgr.add_wallet("alice_btc", "BTC", "bc1qar0srrr7xfkvy5l643lydnw9re59gtzzwf5mdq")

# Retrieve
wallet = mgr.get_wallet("alice_eth")

# List all ETH wallets
eth_wallets = mgr.list_wallets(chain_type="ETH")

# Re-validate
print(mgr.validate_wallet("alice_eth"))

# Statistics
print(mgr.get_stats())
# {"total": 2, "by_chain": {"ETH": 1, "BTC": 1}}
```

---

## Security Philosophy

1. **No private keys stored** — `WalletManager` stores only public addresses.
2. **Validation on ingress** — `add_wallet` rejects invalid addresses before storing.
3. **No network calls** — All validation is pure regex / string matching (stdlib only).
4. **Separation of concerns** — Signing → external HSM/hardware wallet.  
   Broadcasting → `web3` module chain adapters.  
   Address management → this module.

---

## Module Structure

```
wallets/
├── __init__.py           # Public API
├── wallet_validator.py   # WalletValidator (address format checks)
├── wallet_metadata.py    # WalletMetadata, ChainWalletInfo
└── wallet_manager.py     # WalletManager (public address records)
```
