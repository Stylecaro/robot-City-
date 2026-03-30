"""
web3 — Multi-Chain Integration Layer
Provides adapters/connectors for major blockchain networks.
Designed to be extended with additional chains.
"""
from .base_chain import ChainAdapter, ChainType, NetworkConfig, TransactionRecord
from .evm_adapter import EVMAdapter
from .solana_adapter import SolanaAdapter
from .bitcoin_adapter import BitcoinAdapter, LightningAdapter
from .tron_adapter import TronAdapter
from .chain_registry import ChainRegistry

__all__ = [
    "ChainAdapter",
    "ChainType",
    "NetworkConfig",
    "TransactionRecord",
    "EVMAdapter",
    "SolanaAdapter",
    "BitcoinAdapter",
    "LightningAdapter",
    "TronAdapter",
    "ChainRegistry",
]
