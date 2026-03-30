"""
chain_registry.py — Central registry for blockchain chain adapters.

Provides ``ChainRegistry`` for adapter lookup, address validation across
chains, and a convenience factory that pre-populates all default adapters.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .base_chain import ChainAdapter, ChainType
from .bitcoin_adapter import BitcoinAdapter, LightningAdapter
from .evm_adapter import EVMAdapter
from .solana_adapter import SolanaAdapter
from .tron_adapter import TronAdapter


class ChainRegistry:
    """
    A registry that maps ``ChainType`` values to ``ChainAdapter`` instances.

    Usage
    -----
    ::

        registry = ChainRegistry.get_default_registry()
        adapter = registry.get_adapter(ChainType.ETHEREUM)
        print(adapter.validate_address("0xAbc..."))
    """

    def __init__(self) -> None:
        self._adapters: Dict[ChainType, ChainAdapter] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_adapter(self, chain_type: ChainType, adapter: ChainAdapter) -> None:
        """Register *adapter* under *chain_type*, replacing any existing entry."""
        self._adapters[chain_type] = adapter

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------

    def get_adapter(self, chain_type: ChainType) -> ChainAdapter:
        """
        Return the adapter for *chain_type*.

        Raises
        ------
        KeyError
            If no adapter has been registered for *chain_type*.
        """
        if chain_type not in self._adapters:
            raise KeyError(
                f"No adapter registered for {chain_type!r}.  "
                f"Available chains: {[c.value for c in self._adapters]}"
            )
        return self._adapters[chain_type]

    def get_all_chains(self) -> List[ChainType]:
        """Return a list of all currently registered ``ChainType`` values."""
        return list(self._adapters.keys())

    # ------------------------------------------------------------------
    # Validation helper
    # ------------------------------------------------------------------

    def validate_address_on_chain(self, chain_type: ChainType, address: str) -> bool:
        """
        Validate *address* using the adapter registered for *chain_type*.

        Returns ``False`` (rather than raising) if no adapter is found.
        """
        try:
            adapter = self.get_adapter(chain_type)
        except KeyError:
            return False
        return adapter.validate_address(address)

    # ------------------------------------------------------------------
    # Default factory
    # ------------------------------------------------------------------

    @classmethod
    def get_default_registry(cls) -> "ChainRegistry":
        """
        Create and return a ``ChainRegistry`` pre-populated with all
        default chain adapters (no RPC URLs configured).

        Call ``registry.get_adapter(chain_type)`` and then set up your
        own RPC URL before making live on-chain calls.
        """
        registry = cls()
        # EVM chains
        registry.register_adapter(ChainType.ETHEREUM, EVMAdapter.create_ethereum())
        registry.register_adapter(ChainType.POLYGON, EVMAdapter.create_polygon())
        registry.register_adapter(ChainType.BSC, EVMAdapter.create_bsc())
        registry.register_adapter(ChainType.ARBITRUM, EVMAdapter.create_arbitrum())
        registry.register_adapter(ChainType.OPTIMISM, EVMAdapter.create_optimism())
        registry.register_adapter(ChainType.BASE, EVMAdapter.create_base())
        registry.register_adapter(ChainType.AVALANCHE, EVMAdapter.create_avalanche())
        # Non-EVM chains
        registry.register_adapter(ChainType.SOLANA, SolanaAdapter())
        registry.register_adapter(ChainType.BITCOIN, BitcoinAdapter())
        registry.register_adapter(ChainType.LIGHTNING, LightningAdapter())
        registry.register_adapter(ChainType.TRON, TronAdapter())
        return registry

    def __repr__(self) -> str:
        chains = [c.value for c in self._adapters]
        return f"<ChainRegistry chains={chains}>"
